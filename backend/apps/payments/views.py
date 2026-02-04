from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.payments.serializers import PaymentSerializer
from apps.wallets.models import Wallet
from utils.authentication import RequireAPIKey
from utils.external_requests import pawapay_request


User = get_user_model()

class DepositAPIView(APIView):
    """Handles public payments for a specific user"""
    permission_classes = [AllowAny, RequireAPIKey]
    serializer_class = PaymentSerializer

    def post(self, request, id):
        """
        Create a tip and initiate payment for a creator.

        Creates a tip intent and initiates a Mobile Money payment request. This
        endpoint is called when a patron selects an amount (K10, K20, or custom)
        and provides their phone number/provider details.

        Authentication
        --------------
        Guest tipping is supported currently.
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
                {"status": "INVALID_DATA"},
                status=status.HTTP_400_BAD_REQUEST
            )
            wallet = get_object_or_404(Wallet, id=id)
            
            with transaction.atomic():
                payment = serializer.save(wallet=wallet)

            payload = {
                "amount": str(int(payment.amount)),
                "currency": "ZMW",
                "depositId": str(payment.id),
                "payer": {
                    "type": "MMO",
                    "accountDetails": {
                        "provider": str(payment.isp_provider),
                        "phoneNumber": str(payment.patron_phone),
                    },
                },
                "customerMessage": f"Tipping {wallet.creator.user.username}",
                "clientReferenceId": payment.reference,
                "metadata": [
                    {
                        "paymentId": str(payment.id),
                        "walletId": str(wallet.id)
                    }
                ],
            }
            data, code = pawapay_request(
                "POST", "/v2/deposits/", payload=payload)

            if code == 200:
                status_lower = data.get("status", "").lower()
                payment.status = status_lower
                payment.metadata = data
                payment.save()
                serializer = PaymentSerializer(payment)
                return Response(
                    {"status": "ACCEPTED",
                    "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response({"status":"ERROR"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(
            {"status": "INVALID_DATA"},
            status=status.HTTP_400_BAD_REQUEST
        )
