from tests.factories import UserFactory
from apps.wallets.services.wallet_service import WalletService
from utils.exceptions import WalletNotFound, WalletError
import pytest

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
        assert wallet_txn.wallet.balance == Decimal('7')

        #cashout
        wallet_txn = wallet_txn_factory(
            amount=Decimal('-3'), wallet=wallet_txn.wallet, status="COMPLETED",
            transaction_type="PAYOUT")
        wallet_txn.save()
        WalletService.recalculate_wallet_balance(wallet_txn.wallet)
        wallet_txn.wallet.refresh_from_db()
        assert wallet_txn.wallet.balance == Decimal('4')

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
        