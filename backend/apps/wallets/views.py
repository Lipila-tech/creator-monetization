from django.db.models import Sum, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.wallets.models import WalletTransaction, WalletKYC
from apps.payments.models import Payment
from apps.wallets.serializers import (
    WalletDetailSerializer,
    WalletTransactionListSerializer,
    WalletKYCSerializer
)
from utils.external_requests import pawapay_request
from apps.wallets.services.transaction_service import WalletTransactionService
from apps.wallets.services.wallet_service import WalletService
from utils.exceptions import DuplicateTransaction, WalletNotFound
from utils.authentication import RequireAPIKey
from drf_spectacular.utils import extend_schema
from utils import serializers as helpers

class WalletListView(APIView):
    permission_classes = [RequireAPIKey, IsAuthenticated]
    serializer_class = WalletDetailSerializer
    @extend_schema(
        operation_id="retrieve__Wallet",
        summary="Retrieve Users Wallet",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )

    def get(self, request):
        """
        Retrieve the authenticated creator's wallet summary.

        Returns the creator wallet balance, including available and pending balances,
        and currency. Used by the creator dashboard.

        Authentication
        --------------
        Requires authentication (creator).
        """
        try:
            wallet = WalletService.get_wallet_for_user(request.user)
        except WalletNotFound:
            return Response(
                {"status": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch recent CASH_IN transactions
        transactions = WalletTransaction.objects.filter(
            wallet=wallet, transaction_type="CASH_IN"
        ).order_by("-created_at")[:10]

        # Update payment statuses for incomplete payments
        self._update_payment_statuses(wallet)

        # Calculate totals for completed transactions
        totals = WalletTransaction.objects.filter(
            wallet=wallet, status="COMPLETED"
        ).aggregate(
            cash_in=Sum("amount", filter=Q(amount__gt=0)),
            cash_out=Sum("amount",
                        filter=Q(amount__lt=0) & Q(transaction_type="PAYOUT")),
            cash_in_costs=Sum("amount",
                            filter=Q(amount__lt=0) & Q(transaction_type="FEE")),
        )

        # Serialize wallet details
        serializer = WalletDetailSerializer(wallet)
        wallet_data = serializer.data

        # Add transaction summaries and recent transactions
        wallet_data.update({
            "cash_in": totals["cash_in"] or 0,
            "cash_out": abs(totals["cash_out"] or 0),
            "cash_in_costs": abs(totals["cash_in_costs"] or 0),
            "recent_transactions": WalletTransactionListSerializer(
                transactions, many=True
            ).data,
        })

        return Response(
            {"status": "success", "data": wallet_data},
            status=status.HTTP_200_OK
        )

    def _update_payment_statuses(self, wallet):
        """Helper method to update payment statuses from external provider."""
        payments = Payment.objects.filter(wallet=wallet)

        if not payments:
            return

        for payment in payments:
            skip_statuses = [
                "pending",
                "submitted",
                "accepted",
                "processing",
                "in_reconciliation",
            ]
            payment_status = payment.status

            if payment_status.lower() != "completed":
                data, code = pawapay_request(
                    "GET", f"/v2/deposits/{payment.id}"
                )
                if code == 200 and "data" in data:
                    payment_status = data["data"]["status"].lower()

                    if payment_status not in skip_statuses:
                        payment.status = payment_status
                        payment.save()

                    # Process completed payment
                    if payment_status == "completed" and payment.wallet is not None:
                        try:
                            WalletTransactionService.cash_in(
                                wallet=payment.wallet,
                                amount=payment.amount,
                                payment=payment,
                                reference=payment.reference,
                            )
                        except DuplicateTransaction:
                            pass

class WalletTransactionsView(APIView):
    permission_classes = [RequireAPIKey, IsAuthenticated]
    serializer_class = WalletTransactionListSerializer
    @extend_schema(
        operation_id="list_wallet_transactions",
        summary="Retrieve Wallet Transactions",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def get(self, request):
        """
        List transactions for the authenticated creator's wallet.

        Returns a paginated list of wallet transactions including tips received,
        fees, refunds, and payouts. Supports filtering by date, type, and status.

        Authentication
        --------------
        Requires authentication (creator).
        """
        try:
            wallet = WalletService.get_wallet_for_user(request.user)
        except WalletNotFound:
            return Response(
                {"status": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Build filter queryset
        queryset = WalletTransaction.objects.filter(wallet=wallet)

        # Apply optional filters
        transaction_type = request.query_params.get("transaction_type")
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        tx_status = request.query_params.get("status")
        if tx_status:
            queryset = queryset.filter(status=tx_status)

        # Order by creation date (newest first) and apply limit
        limit = int(request.query_params.get("limit", 10))
        transactions = queryset.order_by("-created_at")[:limit]

        serializer = WalletTransactionListSerializer(transactions, many=True)
        return Response(
            {
                "status": "success",
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class WalletKYCView(APIView):
    permission_classes = [RequireAPIKey, IsAuthenticated]
    serializer_class = WalletKYCSerializer
    @extend_schema(
        operation_id="retrieve_wallet_details",
        summary="Retrieve Wallet KYC",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def get(self, request):
        """
        Retrieve details for a specific wallet transaction.

        Returns full transaction details including provider metadata and any
        reconciliation information required for support.

        Authentication
        --------------
        Requires authentication (creator).
        """
        try:
            wallet = WalletService.get_wallet_for_user(request.user)
            wallet_kyc = WalletKYC.objects.get(wallet=wallet)
        except (WalletNotFound, WalletKYC.DoesNotExist):
            return Response(
                {"error": "User does not have wallet KYC information"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WalletKYCSerializer(wallet_kyc)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        operation_id="update_wallet_kyc",
        summary="Update Wallet KYC",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def put(self, request):
        """Update current user's wallet KYC information."""
        try:
            wallet = WalletService.get_wallet_for_user(request.user)
            wallet_kyc = WalletKYC.objects.get(wallet=wallet)
        except (WalletNotFound, WalletKYC.DoesNotExist):
            return Response(
                {"error": "User does not have wallet KYC information"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WalletKYCSerializer(
            wallet_kyc, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )