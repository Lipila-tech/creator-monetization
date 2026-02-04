from decimal import Decimal
import pytest
from apps.wallets.services.transaction_service import\
    WalletTransactionService as WalletTxnService
from utils.exceptions import (
    InsufficientBalance, DuplicateTransaction, InvalidTransaction)
class TestWalletService:
    """Test Single source of truth for all wallet money movements."""

    def test_wallet_balance_matches_transactions(self, user_factory):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("5.00"), payment=None, reference="A"
        )

        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("15.00"), payment=None, reference="B"
        )
        # Only added to transactions if its finalized
        WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("3.00"), correlation_id="C"
        )

        user_factory.creator_profile.wallet.refresh_from_db()
        assert user_factory.creator_profile.wallet.balance == Decimal("18.00")

    def test_cash_in_creates_transaction_and_updates_balance(self, user_factory):
        tx = WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("20.00"),
            payment=None,
            reference="CASHIN-1",
        )
        
        user_factory.creator_profile.wallet.refresh_from_db()
        assert user_factory.creator_profile.wallet.balance == Decimal("18.00")
        assert tx.transaction_type == "CASH_IN"
        assert tx.status == "COMPLETED"

    def test_payout_transaction_reduces_balance(self, user_factory):
        # First cash-in
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("50.00"),
            payment=None,
            reference="CASHIN-2",
        )

        # Payout
        tx = WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("30.00"), correlation_id="PAYOUT-1"
        )

        assert tx.amount == Decimal("-30.00")
        assert tx.status == "PENDING"

    def test_payout_raises_insufficient_balance(self, user_factory):
        with pytest.raises(InsufficientBalance):
            WalletTxnService.payout(
                wallet=user_factory.creator_profile.wallet,
                amount=Decimal("10.00"),
                correlation_id="PAYOUT-FAIL",
            )

    def test_duplicate_transaction_raises(self, user_factory):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("10.00"), payment=None, reference="DUP-1"
        )

        with pytest.raises(DuplicateTransaction):
            WalletTxnService.cash_in(
                wallet=user_factory.creator_profile.wallet,
                amount=Decimal("10.00"),
                payment=None,
                reference="DUP-1",
            )

    def test_finalize_payout_completes_and_updates_balance(self, user_factory):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("50.00"),
            payment=None,
            reference="CASHIN-3",
        )

        payout_tx = WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("30.00"), correlation_id="PAYOUT-2"
        )

        WalletTxnService.finalize_payout(
            payout_tx=payout_tx, success=True)

        user_factory.creator_profile.wallet.refresh_from_db()
        # cashin(50 - 10%) - cashout(k30) - fee(k0)= 8.5
        assert user_factory.creator_profile.wallet.balance == Decimal("15.00")

        payout_tx.refresh_from_db()
        assert payout_tx.status == "COMPLETED"

    def test_finalize_failed_payout_updates_status_but_not_balance(self, user_factory):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("40.00"),
            payment=None,
            reference="CASHIN-4",
        )

        payout_tx = WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("25.00"), correlation_id="PAYOUT-3"
        )

        WalletTxnService.finalize_payout(
            payout_tx=payout_tx, success=False)

        user_factory.creator_profile.wallet.refresh_from_db()
        assert user_factory.creator_profile.wallet.balance == Decimal("36.00")
        payout_tx.refresh_from_db()
        assert payout_tx.status == "FAILED"

    def test_cash_in_creates_transaction_fee(self, user_factory, txn_filter):
        tx = WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("20.00"),
            payment=None,
            reference="CASHIN-FEE-1",
        )

        fee_tx = txn_filter(
            related_transaction=tx, transaction_type="FEE"
        )

        assert fee_tx.amount == Decimal("-2")  # 10% fee
        fees = tx.related_fees.all()
        assert fees.count() == 1
        assert tx.wallet.balance == Decimal("18.00")

    def test_payout_does_not_creates_fee(self, user_factory):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-PAYOUT-FEE",
        )

        payout_tx = WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("30.00"),
            correlation_id="PAYOUT-FEE-TEST",
        )

        fees = payout_tx.related_fees.all()
        assert fees.count() == 0

    def test_finalize_payout_is_idempotent(self, user_factory):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("50.00"),
            payment=None,
            reference="CASHIN-IDEMP",
        )

        payout_tx = WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("20.00"), correlation_id="PAYOUT-IDEMP"
        )

        WalletTxnService.finalize_payout(
            payout_tx=payout_tx, success=True)
        user_factory.creator_profile.wallet.refresh_from_db()
        balance_after_first = user_factory.creator_profile.wallet.balance

        WalletTxnService.finalize_payout(
            payout_tx=payout_tx, success=True)
        user_factory.creator_profile.wallet.refresh_from_db()

        assert user_factory.creator_profile.wallet.balance == balance_after_first

    def test_failed_payout_creates_fee_reversal(self, user_factory, txn_filter):
        WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("40.00"),
            payment=None,
            reference="CASHIN-REVERSAL",
        )

        payout_tx = WalletTxnService.payout(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("20.00"),
            correlation_id="PAYOUT-REVERSAL",
        )
        WalletTxnService.create_fee_transaction(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("5.00"),
            related_transaction=payout_tx,
            reference="reversal")
        WalletTxnService.finalize_payout(
            payout_tx=payout_tx, success=False)

        fee_tx = payout_tx.related_fees.first()
        reversal = txn_filter(
            related_transaction=fee_tx, transaction_type="FEE_REVERSAL"
        )

        assert reversal.amount == abs(fee_tx.amount)

    def test_cash_in_zero_amount_fails(self, user_factory):
        with pytest.raises(InvalidTransaction):
            WalletTxnService.cash_in(
                wallet=user_factory.creator_profile.wallet,
                amount=Decimal("0.00"),
                payment=None,
                reference="ZERO",
            )

    def test_payout_negative_amount_fails(self, user_factory):
        with pytest.raises(InvalidTransaction):
            WalletTxnService.payout(
                wallet=user_factory.creator_profile.wallet,
                amount=Decimal("-5.00"), correlation_id="NEGATIVE"
            )

    def test_finalize_non_payout_raises(self, user_factory):
        tx = WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("10.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )

        with pytest.raises(Exception):
            WalletTxnService.finalize_payout(
                payout_tx=tx, success=True)
