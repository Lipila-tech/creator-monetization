
"""
Service layer for wallet operations, including cash-ins, payouts, and
fee management. This module defines the core business logic for handling
wallet transactions, ensuring data integrity, and maintaining accurate
wallet balances.
"""
import uuid
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, Q
from utils.exceptions import WalletNotFound, WalletError
from datetime import datetime, timedelta
from typing import Optional
from apps.wallets.models import WalletTransaction, Wallet
from apps.payments.services.fee_service import FeeService
from utils.exceptions import (
    InsufficientBalance,
    DuplicateTransaction,
    InvalidTransaction,
)



class PayoutScheduleService:
    """Service to compute next payout date for wallet with funds"""

    @staticmethod
    def get_next_payout_date(
        last_payout_date: Optional[datetime], payout_interval_days: int
    ) -> datetime:
        """
        Computes the next payout date based on the last payout date and
        the payout interval.
        If there has been no previous payout, the next payout date is
        considered to be now (eligible for immediate payout).
        args:
            last_payout_date: the date of the last payout, or None if no payouts yet
            payout_interval_days: the required interval between payouts in days
        returns: the next eligible payout date
        """
        try:
            payout_interval_days = int(payout_interval_days)
        except (ValueError, TypeError):
            raise ValueError("Payout interval must be an integer number of days")
        if payout_interval_days < 0:
            raise ValueError("Payout interval cannot be negative")
        if last_payout_date is None:
            return datetime.now()
        return last_payout_date + timedelta(days=payout_interval_days)


class WalletService:
    """Core wallet operations."""

    @staticmethod
    def get_wallet_for_user(user):
        """Fetches the wallet for a given user.
        Args:
            user (User): The user instance.
        Returns:
            Wallet: The wallet instance associated with the user.
        Raises:
            WalletNotFound: If the user does not have a wallet.
        """
        try:
            return user.creator_profile.wallet
        except Exception:
            raise WalletNotFound("User does not have a wallet")

    @staticmethod
    def recalculate_wallet_balance(wallet):
        """
        Recalculates and updates the wallet balance based on
        completed transactions.
        Args:
            wallet (Wallet): The wallet instance to recalculate balance for.
        Returns:
            Decimal: The updated wallet balance.
        """
        try:
            query_filter = (
                (Q(transaction_type="CASH_IN") | Q(transaction_type="PAYOUT")) &
                Q(status="COMPLETED")
            )
            total = (wallet.transactions.filter(query_filter).aggregate(
                total=Sum("amount"))["total"] or 0)
        except AttributeError:
            raise WalletError("Wallet error")

        wallet.balance = total
        wallet.save(update_fields=["balance"])

        return wallet.balance


class WalletTransactionService:
    """
    Single source of truth for all wallet money movements.
    """
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
        Create a fee (or fee reversal) transaction linked to another
        transaction Amount MUST be positive.
        args:
            wallet: the wallet to which the fee applies
            amount: the fee amount (positive value)
            reference: unique reference for the fee transaction
            related_transaction: the transaction this fee is linked to
            transaction_type: "FEE" for regular fees, "FEE_REVERSAL" for
            reversals
        returns: the created fee transaction (status COMPLETED)
        """
        if amount < 0:
            raise InvalidTransaction("Amount must be positive")
        elif amount == 0:
            final_amount = 0
        else:
            final_amount = -amount if transaction_type == "FEE" else amount

        if WalletTransaction.objects.filter(reference=reference).exists():
            raise DuplicateTransaction("Transaction already exists")
            
        fee_tx = WalletTransaction.objects.create(
            wallet=wallet,
            amount=final_amount,
            transaction_type=transaction_type,
            status="COMPLETED",
            reference=reference,
            related_transaction=related_transaction,
            correlation_id=related_transaction.correlation_id,
        )

        return fee_tx

    @staticmethod
    @transaction.atomic
    def cash_in(*, wallet, amount: Decimal, payment, reference: str):
        """
        Process a cash-in transaction. Amount must be positive.
        args:
        wallet: the wallet to credit
        amount: the gross cash-in amount (before fees)
        payment: the related payment instance (for audit)
        reference: unique reference for the transaction (e.g. payment ID)

        returns: the created cash-in transaction (status COMPLETED). Fees are
        automatically calculated and linked to the cash-in transaction.
        """
        if amount <= 0:
            raise InvalidTransaction("Amount must be positive")
        if WalletTransaction.objects.filter(reference=reference).exists():
            raise DuplicateTransaction("Transaction already exists")

        fee = FeeService.calculate_cash_in_fee(amount)
        net_amount = amount - fee
        
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

    @staticmethod
    @transaction.atomic
    def payout(*, wallet, amount: Decimal, correlation_id: str):
        """
        Initiate a payout transaction. Amount must be positive.
        args:
        wallet: the wallet to debit
        amount: the gross payout amount (before fees)
        correlation_id: unique ID to link payout with external payment
        processor transaction.

        returns: the created payout transaction (status PENDING). Finalization
        of the payout (marking as COMPLETED or FAILED) should be done via
        finalize_payout() to ensure proper fee handling and balance updates.
        """
        
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
        if payout_fee > 0:
            # Fee linked to payout
            WalletTransactionService.create_fee_transaction(
                wallet=wallet,
                amount=payout_fee,
                reference=f"{payout_reference}-FEE",
                related_transaction=payout_tx,
            )

        WalletService.recalculate_wallet_balance(wallet)
        return payout_tx

    @staticmethod
    @transaction.atomic
    def finalize_payout(
        *, payout_tx: WalletTransaction, success: bool, approved_by=None
    ):
        """
        Finalize payout transaction. If success is False, the payout is
        marked as failed and the fee is reversed.
        args:
            payout_tx: the original payout transaction to finalize
            success: whether the payout succeeded or failed
            approved_by: optional user who approved the payout (for audit)
        returns: the updated payout transaction
        """
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
        
        # FAILED PAYOUT → reverse fee
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
