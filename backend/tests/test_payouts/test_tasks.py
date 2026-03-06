from apps.payouts.tasks import auto_payout_wallets
from apps.wallets.models import Wallet
from apps.wallets.services.wallet_services import (
    WalletTransactionService as WalletTxnService,
)
import pytest
from decimal import Decimal
from tests.factories import UserFactory


@pytest.mark.django_db
class TestPayoutTasks:

    def test_auto_payout_wallets(self, admin_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.is_verified = True
        wallet.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-AUTO-PAYOUT",
        )

        auto_payout_wallets()

        payout_tx = wallet.transactions.filter(transaction_type="PAYOUT").first()
        assert payout_tx is not None
        assert payout_tx.status == "PENDING"
        assert payout_tx.amount == Decimal("-90.00")

    def test_auto_payout_wallets_no_balance(self, admin_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.is_verified = True
        wallet.save()

        auto_payout_wallets()

        payout_tx = wallet.transactions.filter(transaction_type="PAYOUT").first()
        assert payout_tx is None

    def test_auto_payout_wallets_unverified_kyc(self, admin_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-AUTO-PAYOUT-UNVERIFIED",
        )

        auto_payout_wallets()

        payout_tx = wallet.transactions.filter(transaction_type="PAYOUT").first()
        assert payout_tx is None

    def test_auto_payout_wallets_pending_payout_exists(self, admin_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.is_verified = True
        wallet.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-AUTO-PAYOUT-PENDING",
        )
        # Create a pending payout transaction to simulate existing payout
        WalletTxnService.payout(
            wallet=wallet,
            amount=Decimal("90.00"),
            correlation_id="TEST-PAYOUT-PENDING",
        )

        with pytest.raises(
            Exception, match="A payout is already pending for this wallet"
        ):
            auto_payout_wallets()

    def test_auto_payout_multiple_wallets(self, admin_user):
        # Create multiple wallets with balance
        UserFactory.create_batch(3)
        for wallet in Wallet.objects.all():
            wallet.is_verified = True
            wallet.save()
            WalletTxnService.cash_in(
                wallet=wallet,
                amount=Decimal("100.00"),
                payment=None,
                reference=f"CASHIN-AUTO-PAYOUT-{wallet.id}",
            )

        auto_payout_wallets()

        for wallet in Wallet.objects.all():
            payout_tx = wallet.transactions.filter(transaction_type="PAYOUT").first()
            assert payout_tx is not None
            assert payout_tx.status == "PENDING"
            assert payout_tx.amount == Decimal("-90.00")

    def test_auto_payout_mixed_wallet_status(self, admin_user):
        # Create verified wallet with balance
        user1 = UserFactory()
        verified_wallet = user1.creator_profile.wallet
        verified_wallet.is_verified = True
        verified_wallet.save()
        WalletTxnService.cash_in(
            wallet=verified_wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-AUTO-PAYOUT-VERIFIED",
        )

        # Create unverified wallet with balance
        user2 = UserFactory()
        unverified_wallet = user2.creator_profile.wallet
        unverified_wallet.is_verified = False
        unverified_wallet.save()
        WalletTxnService.cash_in(
            wallet=unverified_wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-AUTO-PAYOUT-UNVERIFIED",
        )

        auto_payout_wallets()

        # Only verified wallet should have a payout transaction
        payout_tx_verified = verified_wallet.transactions.filter(
            transaction_type="PAYOUT"
        ).first()
        assert payout_tx_verified is not None
        assert payout_tx_verified.status == "PENDING"
        assert payout_tx_verified.amount == Decimal("-90.00")

        payout_tx_unverified = unverified_wallet.transactions.filter(
            transaction_type="PAYOUT"
        ).first()
        assert payout_tx_unverified is None

    def test_auto_payout_mixed_wallet_balances(self, admin_user):
        # Create wallet with balance
        user1 = UserFactory()
        wallet_with_balance = user1.creator_profile.wallet
        wallet_with_balance.is_verified = True
        wallet_with_balance.save()
        WalletTxnService.cash_in(
            wallet=wallet_with_balance,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-AUTO-PAYOUT-WITH-BALANCE",
        )

        # Create wallet without balance
        user2 = UserFactory()
        wallet_without_balance = user2.creator_profile.wallet
        wallet_without_balance.is_verified = True
        wallet_without_balance.save()

        auto_payout_wallets()

        # Only wallet with balance should have a payout transaction
        payout_tx_with_balance = wallet_with_balance.transactions.filter(
            transaction_type="PAYOUT"
        ).first()
        assert payout_tx_with_balance is not None
        assert payout_tx_with_balance.status == "PENDING"
        assert payout_tx_with_balance.amount == Decimal("-90.00")

        payout_tx_without_balance = wallet_without_balance.transactions.filter(
            transaction_type="PAYOUT"
        ).first()
        assert payout_tx_without_balance is None
