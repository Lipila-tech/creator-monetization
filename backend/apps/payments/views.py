from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.payments.serializers import PaymentSerializer
from apps.wallets.models import Wallet
from rest_framework.permissions import AllowAny
from utils.authentication import RequireAPIKey
from utils.external_requests import limopay_request
from drf_spectacular.utils import extend_schema
from django.conf import settings
from utils import serializers as helpers

User = get_user_model()

LIMOPAY_WALLET_ID = settings.LIMOPAY_WALLET_ID
class DepositAPIView(APIView):
    permission_classes = [AllowAny, RequireAPIKey]
    serializer_class = PaymentSerializer

    @extend_schema(
        operation_id="send_donation",
        summary="Send Donation",
        responses={
            201: helpers.CreatedResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def post(self, request, wallet_id):
        """
        Creates a donation intent and initiates a Mobile Money payment request. This
        endpoint is called after a patron selects an amount (K10, K20, or custom)
        provides their phone number and selects provider then clicks send.

        Authentication
        --------------
        Guest donation is  currently supported.
        Optional:Authenticated patron(future).

        If guest is supported, return a receipt without attaching a user identity.
        """
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            from utils.validators import PhoneValidator as PV
            phone = serializer.validated_data.get("patron_phone")
            is_valid, msg = PV.validate_phone_number(phone)
            if not is_valid:
                return Response(
                    {
                        "status": "failed",
                        "error": "validation_error",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            wallet = get_object_or_404(Wallet, id=wallet_id)
            
            with transaction.atomic():
                payment = serializer.save(wallet=wallet)

            payload = {
                "amount": str(int(payment.amount)),
                "currency": "ZMW",
                "depositId": str(payment.id),
                "payer": {
                    "type": "MMO",
                    "accountDetails": {
                        "provider": str(payment.provider),
                        "phoneNumber": '26' + str(payment.patron_phone),
                    },
                },
                "customerMessage": "Donating at TipZed",
                "clientReferenceId": payment.reference,
                "metadata": [
                    {
                        "paymentId": str(payment.id),
                        "walletId": str(wallet.id)
                    }
                ],
            }

            data, code = limopay_request(
                "POST", f"/api/v1/payments/mobile-money/{wallet_id}/", payload=payload)
            # Treat any 2xx as success from the gateway
            if 200 <= code < 300:
                # Map Limopay response to local payment fields
                gw_status = (data.get("status") or "").lower() if isinstance(data, dict) else ""
                if gw_status == "success":
                    payment.status = "accepted"
                else:
                    payment.status = gw_status or payment.status
                # Limopay returns transaction_id on success
                if isinstance(data, dict) and data.get("transaction_id"):
                    payment.external_id = data.get("transaction_id")
                payment.metadata = data
                payment.save()
                serializer = PaymentSerializer(payment)
                return Response(
                    {"status": "accepted",
                     "data": serializer.data
                     },
                    status=status.HTTP_201_CREATED
                )
            # Forward gateway error
            try:
                return Response({"status": data.get('status', 'error')}, status=code)
            except Exception:
                return Response({"status": "error"}, status=code)

        return Response(
            {
                "status": "failed",
                "error": "validation_error",
            },
            status=status.HTTP_400_BAD_REQUEST
        )
