from decimal import Decimal
import uuid
from django.db import transaction
from django.core.exceptions import PermissionDenied
from apps.wallets.services.transaction_service import WalletTransactionService
from apps.wallets.services.fee_service import FeeService
from apps.wallets.services.wallet_service import WalletService
from utils.exceptions import InsufficientBalance, InvalidTransaction


class PayoutOrchestrator:
    """Orchestrates the payout process for wallets."""

    PAYOUT_FEE = Decimal("10.00")

    @staticmethod
    @transaction.atomic
    def initiate_payout(*, wallet, initiated_by):
        """
        Initiate a payout for the entire wallet balance.
        Args:
            wallet (Wallet): The wallet to payout from.
            initiated_by (User): The user initiating the payout.
        Returns:
            WalletTransaction: The payout transaction created.
        Raises:
            PermissionDenied: If the user is not staff.
            InsufficientBalance: If the wallet has insufficient balance.
        """
        if not wallet.kyc.verified:
            raise InvalidTransaction("KYC not verified. Payouts are blocked.")

        if not initiated_by.is_staff:
            raise PermissionDenied("Only staff can payout")

        WalletService.recalculate_wallet_balance(wallet)

        if wallet.balance <= 0:
            raise InsufficientBalance("No balance to payout")

        correlation_id = f"PAYOUT-{uuid.uuid4()}"

        payout_tx = WalletTransactionService.payout(
            wallet=wallet,
            amount=wallet.balance - FeeService.payout_fee(),  # Deduct fee
            correlation_id=f"{correlation_id}-MAIN",
        )

        return payout_tx

    @staticmethod
    @transaction.atomic
    def finalize(*, payout_tx, success: bool, approved_by=None):
        return WalletTransactionService.finalize_payout(
            payout_tx=payout_tx, success=success, approved_by=approved_by
        )
