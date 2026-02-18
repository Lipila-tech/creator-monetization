import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from apps.wallets.services.wallet_services import (
    WalletService, PayoutScheduleService)
from apps.wallets.services.wallet_services import\
    WalletTransactionService as WalletTxnService
from utils.exceptions import (
    InsufficientBalance, DuplicateTransaction,
    InvalidTransaction,WalletNotFound, WalletError)
from tests.factories import UserFactory


class TestPayoutScheduleService:
    """Test Service to compute next payout date for wallet with funds"""

    def test_get_next_payout_date_no_previous_payout(self):
        """Test that if there is no previous payout, the next payout date is now."""
        next_date = PayoutScheduleService.get_next_payout_date(
            last_payout_date=None, payout_interval_days=7
        )
        assert isinstance(next_date, datetime)

    def test_get_next_payout_date_with_previous_payout(self):
        """Test that the next payout date is correctly calculated
        based on the last payout date and interval."""
        last_payout = datetime(2024, 1, 1)
        next_date = PayoutScheduleService.get_next_payout_date(
            last_payout_date=last_payout, payout_interval_days=7
        )
        assert next_date == last_payout + timedelta(days=7)

    def test_get_next_payout_date_with_previous_payout_and_zero_interval(self):
        """If payout interval is zero, next payout date should be same as last
        payout date."""
        last_payout = datetime(2024, 1, 1)
        next_date = PayoutScheduleService.get_next_payout_date(
            last_payout_date=last_payout, payout_interval_days=0
        )
        assert next_date == last_payout


    def test_get_next_payout_date_with_previous_payout_and_large_interval(self):
        """Test that the next payout date is correctly calculated for a large
        interval."""
        last_payout = datetime(2024, 1, 1)
        next_date = PayoutScheduleService.get_next_payout_date(
            last_payout_date=last_payout, payout_interval_days=30
        )
        assert next_date == last_payout + timedelta(days=30)

    def test_get_next_payout_date_with_previous_payout_and_non_integer_interval(self):
        """Test that the next payout date is correctly calculated for a non-integer
        interval (should be treated as integer)."""
        last_payout = datetime(2024, 1, 1)
        next_date = PayoutScheduleService.get_next_payout_date(
            last_payout_date=last_payout, payout_interval_days=7.5
        )
        assert next_date == last_payout + timedelta(days=7)

    def test_get_next_payout_date_with_previous_payout_and_non_numeric_interval(self):
        """Test that if the payout interval is non-numeric, it raises a TypeError."""
        last_payout = datetime(2024, 1, 1)
        with pytest.raises(ValueError):
            PayoutScheduleService.get_next_payout_date(
                last_payout_date=last_payout, payout_interval_days="seven"
            )

    def test_get_next_payout_date_with_previous_payout_and_none_interval(self):
        """Test that if the payout interval is None, it raises a TypeError."""
        last_payout = datetime(2024, 1, 1)
        with pytest.raises(ValueError):
            PayoutScheduleService.get_next_payout_date(
                last_payout_date=last_payout, payout_interval_days=None
            )

    def test_get_next_payout_date_with_previous_payout_and_negative_interval(self):
        """Test that if the payout interval is negative, it raises a ValueError."""
        last_payout = datetime(2024, 1, 1)
        with pytest.raises(ValueError):
            PayoutScheduleService.get_next_payout_date(
                last_payout_date=last_payout, payout_interval_days=-7
            )
    

class TestWalletTransactionService:
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

    def test_cash_in_creates_transaction_and_updates_wallet_balance(self, user_factory):
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


    def test_cash_in_creates_a_transaction_with_deducted_fee(self, user_factory):
        tx = WalletTxnService.cash_in(
            wallet=user_factory.creator_profile.wallet,
            amount=Decimal("20.00"),
            payment=None,
            reference="CASHIN-1",
        )
        
        user_factory.creator_profile.wallet.refresh_from_db()
        wallet_balance = user_factory.creator_profile.wallet.balance
        assert wallet_balance == tx.amount
        

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
        # cashin(50 - 10%) = 45 - cashout(30) = 15
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


@pytest.mark.django_db
class TestWalletService:
    def test_get_wallet_for_user(self, user_factory):
        wallet = WalletService.get_wallet_for_user(user_factory)
        assert wallet == user_factory.creator_profile.wallet

    def test_get_wallet_for_user_with_no_wallet(self):
        user = UserFactory(user_type="admin")

        with pytest.raises(WalletNotFound, match="User does not have a wallet"):
            WalletService.get_wallet_for_user(user)
        
    def test_recalculate_wallet_balance_cash_in_out(self, wallet_txn_factory):
        from decimal import Decimal
        wallet_txn = wallet_txn_factory(
            amount=Decimal('10'), status="COMPLETED")
        WalletService.recalculate_wallet_balance(wallet_txn.wallet)
        wallet_txn.wallet.refresh_from_db()
        assert wallet_txn.wallet.balance == Decimal('10')

        # Add fee
        wallet_txn = wallet_txn_factory(
            amount=Decimal('-3'), wallet=wallet_txn.wallet, status="COMPLETED",
            transaction_type="FEE")
        wallet_txn.save()
        WalletService.recalculate_wallet_balance(wallet_txn.wallet)
        wallet_txn.wallet.refresh_from_db()
        assert wallet_txn.wallet.balance == Decimal('10')

        #cashout
        wallet_txn = wallet_txn_factory(
            amount=Decimal('-3'), wallet=wallet_txn.wallet, status="COMPLETED",
            transaction_type="PAYOUT")
        wallet_txn.save()
        WalletService.recalculate_wallet_balance(wallet_txn.wallet)
        wallet_txn.wallet.refresh_from_db()
        assert wallet_txn.wallet.balance == Decimal('7')

    def test_dont_add_pending_txn_to_balance(self, wallet_txn_factory):
        from decimal import Decimal
        wallet_txn = wallet_txn_factory(
            amount=Decimal('10'), status="COMPLETED")
        WalletService.recalculate_wallet_balance(wallet_txn.wallet)
        wallet_txn.wallet.refresh_from_db()
        assert wallet_txn.wallet.balance == Decimal('10')

        wallet_txn = wallet_txn_factory(
            amount=Decimal('-3'), wallet=wallet_txn.wallet)
        wallet_txn.save()
        WalletService.recalculate_wallet_balance(wallet_txn.wallet)
        wallet_txn.wallet.refresh_from_db()
        assert wallet_txn.wallet.balance == Decimal('10')

    def test_calculate_balance_bad_arguments(self, wallet_txn_factory):
        from decimal import Decimal
        wallet_txn_factory(
            amount=Decimal('10'), status="COMPLETED")
        with pytest.raises(WalletError):
            WalletService.recalculate_wallet_balance('not-wallet')
        