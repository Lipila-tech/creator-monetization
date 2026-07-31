import json
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apps.payments.models import Payment
from apps.payments.models import PaymentWebhookLog as WebHook
from apps.wallets.services.wallet_services import WalletTransactionService
from utils.authentication import RequireAPIKey
from utils.exceptions import DuplicateTransaction
from utils.external_requests import limopay_request
User = get_user_model()


class WebhookAPIView(APIView):
    """Handles pawapay deposit Callback requests"""

    authentication_classes = []
    permission_classes = []

    @extend_schema(exclude=True)
    def post(self, request):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Support both old pawapay shape and new Limopay shape
        data = payload.get("data") if isinstance(payload, dict) and payload.get("data") else payload

        # Extract fields from nested data if present
        deposit_id = data.get("depositId") or data.get("reference")
        res_status = (data.get("status") or payload.get("status") or "").lower()
        external_id = data.get("id") or data.get("providerTransactionId")

        if not all([deposit_id, res_status]):
            return Response(
                {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
            )

        res_status = res_status.lower()

        # IDEMPOTENCY CHECK - prefer external_id when available
        if external_id and WebHook.objects.filter(external_id=external_id).exists():
            return Response(
                {"message": "Duplicate callback ignored"}, status=status.HTTP_200_OK
            )
        try:
            with transaction.atomic():
                # Try to resolve by reference first, fallback to UUID id
                try:
                    payment = Payment.objects.select_for_update().get(reference=deposit_id)
                except Payment.DoesNotExist:
                    payment = Payment.objects.select_for_update().get(id=deposit_id)

                # Dont update status if pending/submitted/accepted to
                # avoid overwriting final state
                skip_statuses = [
                    "pending",
                    "submitted",
                    "accepted",
                    "processing",
                    "in_reconciliation",
                ]
                if res_status in skip_statuses:
                    res_status = payment.status
                payment.status = res_status
                # store gateway id if present
                if external_id:
                    payment.external_id = external_id
                payment.provider_data = data
                payment.save()

                # Create webhook log ONCE, include raw payload
                WebHook.objects.create(
                    raw_payload=json.dumps(payload),
                    parsed_payload=data if isinstance(data, dict) else {"data": data},
                    event_type=f"deposit.{res_status}",
                    payment=payment,
                    provider=payment.provider,
                    external_id=external_id or "",
                )
                if res_status == "completed" and payment.wallet is not None:
                    try:
                        WalletTransactionService.cash_in(
                            wallet=payment.wallet,
                            amount=payment.amount,
                            payment=payment,
                            reference=external_id or payment.reference,
                        )
                    except DuplicateTransaction:
                        pass

        except Payment.DoesNotExist:
            return Response({"status": "NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            # If unique constraint triggered by race condition or other parsing errors
            return Response(
                {"message": "Duplicate callback ignored"}, status=status.HTTP_200_OK
            )
        return Response({"message": "Callback processed"}, status=status.HTTP_200_OK)


class PaymentStatusAPIView(APIView):
    """Endpoint to get payment status by deposit id"""

    authentication_classes = []
    permission_classes = [RequireAPIKey, AllowAny]

    @extend_schema(
        operation_id="retrieve_payment_status",
        summary="Retrieve Payment Status",
        description="Get payment status by deposit ID",
        parameters=[
            {
                "name": "deposit_id",
                "description": "ID of the deposit to check status for",
                "required": True,
                "type": "string (uuid)",
            }
        ],
        responses={
            200: {"description": "Payment status retrieved successfully"},
            404: {"description": "Payment not found"},
        },
    )
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=str(payment_id))
            final_statuses = ["completed", "failed", "rejected"]
            if payment.status in final_statuses:
                return Response({"status": payment.status}, status=status.HTTP_200_OK)
            
            # Use payment.reference when asking gateway for latest status 
            data, code = limopay_request("GET", f"/api/v1/payments/{payment.reference}/")
            if 200 <= code < 300:
                # Assume gateway returns a status field
                return Response(
                    {"status": (data.get("status") or "").lower()}, status=status.HTTP_200_OK
                )
            return Response({"status": "error"}, status=code)
        except Payment.DoesNotExist:
            return Response({"status": "NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
