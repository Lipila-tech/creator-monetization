from decimal import Decimal
from django.core.exceptions import PermissionDenied
import pytest
from apps.payments.services.payout_orchestrator import PayoutOrchestrator
from utils.exceptions import InsufficientBalance, InvalidTransaction
from apps.wallets.services.transaction_service import\
    WalletTransactionService as WalletTxnService
from apps.wallets.models import WalletTransaction
class TestPayoutOrchestratorTest:

    def test_staff_cannot_initiate_payout_unverified_kyc(self, staff_user, user_factory):
        wallet = user_factory.creator_profile.wallet
      
        with pytest.raises(InvalidTransaction, match="KYC not verified. Payouts are blocked"):
            PayoutOrchestrator.initiate_payout(
                wallet=wallet,
                initiated_by=staff_user,
            )
    
    def test_staff_can_initiate_payout_verified_wallet(self, staff_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )
        payout_tx = PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=staff_user,
        )

        assert payout_tx.transaction_type == "PAYOUT"
        assert payout_tx.status == "PENDING"
        assert payout_tx.amount == Decimal("-90.00")

    def test_non_staff_cannot_initiate_payout(self, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )

        with pytest.raises(PermissionDenied):
            PayoutOrchestrator.initiate_payout(
                wallet=wallet,
                initiated_by=user_factory,
            )

    def test_cannot_payout_zero_balance(self, staff_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
      
        with pytest.raises(InsufficientBalance):
            PayoutOrchestrator.initiate_payout(
                wallet=wallet,
                initiated_by=staff_user,
            )

    def test_payout_fee_is_deducted(self, staff_user, user_factory, txn_filter):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )
        payout_tx = PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=staff_user,
        )

        fee_tx = txn_filter(
            transaction_type="FEE", related_transaction=payout_tx
        )

        assert fee_tx is not None
        assert fee_tx.amount == Decimal("0.00")
        assert fee_tx.status == "COMPLETED"

    def test_finalize_successful_payout(self, staff_user, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )

        payout_tx = PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=staff_user,
        )

        PayoutOrchestrator.finalize(payout_tx=payout_tx, success=True)

        payout_tx.refresh_from_db()
        wallet.refresh_from_db()

        assert payout_tx.status == "COMPLETED"
        assert user_factory.creator_profile.wallet.balance == Decimal("0.00")

    def test_failed_payout_reverses_fee(self, staff_user, user_factory, txn_filter):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )

        payout_tx = PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=staff_user,
        )

        PayoutOrchestrator.finalize(payout_tx=payout_tx, success=False)

        wallet.refresh_from_db()
        payout_tx.refresh_from_db()

        assert payout_tx.status == "FAILED"
        assert user_factory.creator_profile.wallet.balance == Decimal("90.00")

        assert txn_filter(transaction_type="FEE_REVERSAL") is not None

    def test_finalize_is_idempotent(self, staff_user, user_factory, txn_filter):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        WalletTxnService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="CASHIN-NOT-PAYOUT",
        )

        payout_tx = PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=staff_user,
        )

        PayoutOrchestrator.finalize(payout_tx=payout_tx, success=False)

        # Call again (should not create duplicate reversals)
        PayoutOrchestrator.finalize(payout_tx=payout_tx, success=False)

        assert WalletTransaction.objects.filter(transaction_type="FEE_REVERSAL").count() == 1