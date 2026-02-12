import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apps.payments.models import Payment
from apps.payments.models import PaymentWebhookLog as WebHook
from apps.wallets.services.transaction_service import WalletTransactionService
from utils.authentication import RequireAPIKey
from utils.exceptions import DuplicateTransaction
from utils.external_requests import pawapay_request

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

        deposit_id = payload.get("depositId")
        res_status = payload.get("status").lower()
        external_id = payload.get("providerTransactionId")

        if not all([deposit_id, res_status]):
            return Response(
                {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
            )

        res_status = res_status.lower()

        # IDEMPOTENCY CHECK (fast path) - check for duplicate based on external_id
        if external_id and WebHook.objects.filter(external_id=external_id).exists():
            return Response(
                {"message": "Duplicate callback ignored"}, status=status.HTTP_200_OK
            )
        try:
            with transaction.atomic():
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
                payment.save()

                # Create webhook log ONCE
                WebHook.objects.create(
                    parsed_payload=payload,
                    event_type=f"deposit.{res_status}",
                    payment=payment,
                    provider=payment.provider,
                    external_id=external_id,
                )
                if res_status == "completed" and payment.wallet is not None:
                    try:
                        WalletTransactionService.cash_in(
                            wallet=payment.wallet,
                            amount=payment.amount,
                            payment=payment,
                            reference=external_id,
                        )
                    except DuplicateTransaction:
                        pass

        except Payment.DoesNotExist:
            return Response({"status": "NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            # If unique constraint triggered by race condition
            return Response(
                {"message": "Duplicate callback ignored"}, status=status.HTTP_200_OK
            )
        return Response({"message": "Callback processed"}, status=status.HTTP_200_OK)


def resend_callback(deposit_id):
    """Helper function to resend callback for a given deposit id
    ARgs:
        deposit_id (str): ID of the deposit to resend callback for
    Returns:        tuple: (response data, status code) from the callback resend request
    """
    data, code = pawapay_request("POST", f"/v2/deposits/resend-callback/{deposit_id}")
    return data, code

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
            # Check if payment has received a callback before returning status
            if not WebHook.objects.filter(
                payment=payment,
                event_type__in=[
                    "deposit.completed",
                    "deposit.failed",
                    "deposit.rejected",
                ],
            ).exists():
                data, code = resend_callback(str(payment_id))
                if code == 200:
                    return Response(
                        {"status": data["status"].lower()}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"status": "error"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            return Response({"status": payment.status}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({"status": "NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
