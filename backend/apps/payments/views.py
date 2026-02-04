from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.payments.serializers import PaymentSerializer
from apps.wallets.models import Wallet
from utils.external_requests import pawapay_request
from utils.authentication import RequireAPIKey


User = get_user_model()

class DepositAPIView(APIView):
    """Handles public payments for a specific user"""
    permission_classes = [AllowAny, RequireAPIKey]
    serializer_class = PaymentSerializer

    def post(self, request, id):
        """Create a new deposit payment"""

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            wallet = get_object_or_404(Wallet, id=id)
            if not wallet:
                return Response(
                    {
                        "status": "rejected",
                        "message": "User has no wallet to collect payment.",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                payment = serializer.save()

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
                {"status": "success",
                 "data": serializer.data
                 },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"status": "INVALID_DATA"},
            status=status.HTTP_400_BAD_REQUEST
        )
