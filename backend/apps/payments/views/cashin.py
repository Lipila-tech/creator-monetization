from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.wallets.models import Tier, WalletKYC
from apps.wallets.services.wallet_service import WalletService
from apps.wallets.services.transaction_service import WalletTransactionService
from utils.external_requests import pawapay_request
from utils.exceptions import DuplicateTransaction

User = get_user_model()


class AvailabilityAPIView(APIView):
    """Checks Mobile money providers availability"""
    permission_classes = [AllowAny]

    def get(self, request):
        data, code = pawapay_request(
            "GET", "/availability?country=ZMB&operationType=DEPOSIT"
        )
        return Response(data, status=code)


class ActiveConfigAPIView(APIView):
    """Gets recommended active configuration"""
    permission_classes = [AllowAny]

    def get(self, request):
        data, code = pawapay_request(
            "GET", "/active-conf?country=ZMB&operationType=DEPOSIT"
        )
        return Response(data, status=code)


class ResendCallbackAPIView(APIView):
    """Resends the deposit callback for a given deposit ID"""
    permission_classes = [IsAuthenticated]

    def post(self, request, deposit_id):
        data, code = pawapay_request(
            "POST", f"/v2/deposits/resend-callback/{deposit_id}"
        )
        return Response(data, status=code)


class PaymentStatusAPIView(APIView):
    """Handles the payment status for a given deposit ID"""
    permission_classes = [AllowAny]

    def get(self, request, deposit_id):
        payment = Payment.objects.filter(id=deposit_id).first()

        context = {
            "status": "Unknown",
            "message": "Unknown status",
            "statuses": []
        }

        if not payment:
            return Response(
                {
                    "status": "failed",
                    "message": "An error occurred. Please try again later.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if payment.status == "rejected":
            try:
                failure_msg = payment.metadata["failureReason"]["failureMessage"]
            except (KeyError, TypeError):
                failure_msg = "Unspecified Failure"

            return Response(
                {
                    "status": "rejected",
                    "message": failure_msg,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data, code = pawapay_request("GET", f"/v2/deposits/{deposit_id}")

        if code == 200 and "data" in data:
            status_lower = data["data"]["status"].lower()
            skip_statuses = [
                "pending",
                "submitted",
                "accepted",
                "processing",
                "in_reconciliation",
            ]

            if payment.status in skip_statuses and status_lower in skip_statuses:
                status_lower = payment.status

            payment.status = status_lower
            payment.metadata = data["data"]
            payment.save()

            try:
                failure_msg = payment.metadata["failureReason"]["failureMessage"]
            except (KeyError, TypeError):
                failure_msg = "Unspecified Failure"

            if status_lower in skip_statuses:
                message = "Approve transaction from PAWAPAY on your mobile device"
            elif status_lower == "completed":
                message = "Transaction Completed"
            else:
                message = failure_msg

            return Response(
                {
                    "status": status_lower,
                    "message": message,
                    "statuses": skip_statuses,
                }
            )

        return Response(context)


class DepositAPIView(APIView):
    """Handles payments for a specific user"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        """Get deposit tier information"""
        user = get_object_or_404(User, slug=slug)
        tier = get_object_or_404(Tier, creator=user.creator_profile)
        tiers = WalletKYC.objects.filter(wallet__creator=tier.creator).first()


        return Response({
            "tier": {
                "id": tier.id,
                "subtotal": str(tier.subtotal()),
                "status": tier.status,
            },
            "kyc": {
                "id": tiers.id if tiers else None,
            } if tiers else None,
        })

    def post(self, request, slug):
        """Create a new deposit payment"""
        user = get_object_or_404(User, slug=slug)
        tier = get_object_or_404(Tier, creator=user.creator_profile)

        amount = tier.subtotal()
        phone_number = request.data.get("phoneNumber")
        provider = request.data.get("provider")
        isp_provider = request.data.get("ispProvider")

        if not phone_number:
            return Response(
                {"error": "phoneNumber is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        wallet = WalletService.get_wallet_for_user(user)
        if not wallet:
            return Response(
                {
                    "status": "rejected",
                    "message": "User has no wallet to collect payment.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            payment = Payment.objects.create_payment(
                amount=amount,
                customer_phone=f"260{phone_number}",
                provider=provider or "pawapay",
                isp_provider=isp_provider,
                wallet=wallet,
            )

        payload = {
            "amount": str(int(amount)),
            "currency": "ZMW",
            "depositId": str(payment.id),
            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "provider": str(payment.isp_provider),
                    "phoneNumber": str(payment.customer_phone),
                },
            },
            "customerMessage": "Payment to SchaAdmin",
            "clientReferenceId": payment.reference,
            "metadata": [
                {
                    "paymentId": str(payment.id),
                    "tierId": str(tier.id)
                }
            ],
        }

        data, code = pawapay_request("POST", "/v2/deposits/", payload=payload)

        if code == 200:
            status_lower = data.get("status", "").lower()
            payment.status = status_lower
            payment.metadata = data
            payment.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DepositCallbackAPIView(APIView):
    """Handles Deposit Callback requests from PAWAPAY"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            payload = request.data
        except Exception:
            return Response(
                {"error": "Invalid JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deposit_id = payload.get("depositId")
        status_lower = payload.get("status")
        external_id = payload.get("providerTransactionId")

        if not all([deposit_id, status_lower]):
            return Response(
                {"error": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST
            )

        status_lower = status_lower.lower()

        # IDEMPOTENCY CHECK - check for duplicate based on external_id
        from apps.payments.models import WebHook
        if external_id and WebHook.objects.filter(
                external_id=external_id).exists():
            return Response(
                {"message": "Duplicate callback ignored"},
                status=status.HTTP_200_OK
            )

        try:
            with transaction.atomic():
                payment = Payment.objects.select_for_update().get(id=deposit_id)

                skip_statuses = [
                    "pending",
                    "submitted",
                    "accepted",
                    "processing",
                    "in_reconciliation",
                ]

                if status_lower in skip_statuses:
                    status_lower = payment.status

                payment.status = status_lower
                payment.save()

                WebHook.objects.create(
                    parsed_payload=payload,
                    event_type=f"deposit.{status_lower}",
                    payment=payment,
                    provider=payment.provider,
                    external_id=external_id,
                )

                if status_lower == "completed" and payment.wallet is not None:
                    try:
                        WalletTransactionService.cash_in(
                            wallet=payment.wallet,
                            amount=payment.amount,
                            payment=payment,
                            reference=external_id,
                        )
                        try:
                            tier = Tier.objects.filter(
                                payment=payment).first()
                            if tier:
                                tier.status = status_lower
                                tier.save()
                        except Exception:
                            pass
                    except DuplicateTransaction:
                        pass

        except Payment.DoesNotExist:
            return Response(
                {"status": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception:
            return Response(
                {"message": "Duplicate callback ignored"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Callback processed"},
            status=status.HTTP_200_OK
        )