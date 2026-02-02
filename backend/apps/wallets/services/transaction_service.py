import uuid
from decimal import Decimal
from django.db import transaction

from apps.wallets.models.payment_related import WalletTransaction, Wallet
from utils.exceptions import (
    InsufficientBalance,
    DuplicateTransaction,
    InvalidTransaction,
)
from apps.wallets.services.wallet_service import WalletService
from apps.wallets.services.fee_service import FeeService


class WalletTransactionService:
    """
    Single source of truth for all wallet money movements.
    """

    # ------------------------------------------------------------------
    # FEE CREATION (shared utility)
    # ------------------------------------------------------------------
    @staticmethod
    def create_fee_transaction(
        *,
        wallet,
        amount: Decimal,
        reference: str,
        related_transaction: WalletTransaction,
        transaction_type: str = "FEE",
    ) -> WalletTransaction:
        """
        Create a fee (or fee reversal)
        transaction linked to another transaction.
        Amount MUST be positive.
        """
        if amount <= 0:
            raise InvalidTransaction("Fee amount must be positive")

        if WalletTransaction.objects.filter(reference=reference).exists():
            raise DuplicateTransaction("Transaction already exists")

        fee_tx = WalletTransaction.objects.create(
            wallet=wallet,
            amount=-amount if transaction_type == "FEE" else amount,
            transaction_type=transaction_type,
            status="COMPLETED",
            reference=reference,
            related_transaction=related_transaction,
            correlation_id=related_transaction.correlation_id,
        )

        return fee_tx

    # ------------------------------------------------------------------
    # CASH-IN
    # ------------------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def cash_in(*, wallet, amount: Decimal, payment, reference: str):
        if amount <= 0:
            raise InvalidTransaction("Amount must be positive")
        if WalletTransaction.objects.filter(reference=reference).exists():
            raise DuplicateTransaction("Transaction already exists")

        fee = FeeService.calculate_cash_in_fee(amount)
        net_amount = amount

        correlation_id = f"CASHIN-{uuid.uuid4()}"

        cashin_tx = WalletTransaction.objects.create(
            wallet=wallet,
            amount=net_amount,
            transaction_type="CASH_IN",
            status="COMPLETED",
            payment=payment,
            reference=reference,
            correlation_id=correlation_id,
        )

        # Fee linked to cash-in
        if fee > 0:
            WalletTransactionService.create_fee_transaction(
                wallet=wallet,
                amount=fee,
                reference=f"{reference}-FEE",
                related_transaction=cashin_tx,
            )

        WalletService.recalculate_wallet_balance(wallet)
        return cashin_tx

    # ------------------------------------------------------------------
    # PAYOUT (INITIATE)
    # ------------------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def payout(*, wallet, amount: Decimal, correlation_id: str):
        if amount <= 0:
            raise InvalidTransaction("Amount must be positive")

        payout_fee = FeeService.payout_fee()
        total_required = amount + payout_fee
        wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)
        WalletService.recalculate_wallet_balance(wallet)

        if wallet.balance < total_required:
            raise InsufficientBalance(
                f"Insufficient balance. Required\
                      {total_required}, available {wallet.balance}"
            )

        payout_reference = f"PAYOUT-{uuid.uuid4()}"

        payout_tx = WalletTransaction.objects.create(
            wallet=wallet,
            amount=-amount,
            transaction_type="PAYOUT",
            status="PENDING",
            reference=payout_reference,
            correlation_id=correlation_id,
        )

        # Fee linked to payout
        WalletTransactionService.create_fee_transaction(
            wallet=wallet,
            amount=payout_fee,
            reference=f"{payout_reference}-FEE",
            related_transaction=payout_tx,
        )

        WalletService.recalculate_wallet_balance(wallet)
        return payout_tx

    # ------------------------------------------------------------------
    # PAYOUT (FINALISE)
    # ------------------------------------------------------------------
    @staticmethod
    @transaction.atomic
    def finalize_payout(
        *, payout_tx: WalletTransaction, success: bool, approved_by=None
    ):
        if payout_tx.transaction_type != "PAYOUT":
            raise InvalidTransaction("Not a payout transaction")

        if payout_tx.status != "PENDING":
            return payout_tx  # idempotent

        payout_tx.approved_by = approved_by

        if success:
            payout_tx.status = "COMPLETED"
            payout_tx.save(update_fields=["status", "approved_by"])
            WalletService.recalculate_wallet_balance(payout_tx.wallet)
            return payout_tx

        # -------------------------
        # FAILED PAYOUT → reverse fee
        # -------------------------
        payout_tx.status = "FAILED"
        payout_tx.save(update_fields=["status", "approved_by"])

        fee_tx = payout_tx.related_fees.filter(
            transaction_type="FEE",
            status="COMPLETED",
        ).first()

        if fee_tx:
            WalletTransactionService.create_fee_transaction(
                wallet=payout_tx.wallet,
                amount=abs(fee_tx.amount),
                reference=f"{fee_tx.reference}-REVERSAL",
                related_transaction=fee_tx,
                transaction_type="FEE_REVERSAL",
            )

        WalletService.recalculate_wallet_balance(payout_tx.wallet)
        return payout_tx
