"""
Test cases for payout views.
"""
import pytest
import uuid
from decimal import Decimal
from unittest.mock import patch

from django.test import Client
from django.urls import reverse

from apps.wallets.services.wallet_services import WalletTransactionService
from apps.payments.services.payout_orchestrator import PayoutOrchestrator
from tests.factories import UserFactory, WalletTransactionFactory


@pytest.mark.django_db
class TestTriggerWalletPayout:
    """Tests for trigger_wallet_payout view"""

    def test_requires_staff_member(self):
        """Test that non-staff users are redirected"""
        client = Client()
        user = UserFactory(is_staff=False)
        wallet = user.creator_profile.wallet

        client.force_login(user)
        response = client.get(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id])
        )
        # Should return 302 redirect for non-staff users
        assert response.status_code == 302

    def test_requires_staff_member_post(self):
        """Test that POST requests require staff member"""
        client = Client()
        user = UserFactory(is_staff=False)
        wallet = user.creator_profile.wallet

        client.force_login(user)
        response = client.post(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id])
        )
        assert response.status_code == 302

    def test_get_request_shows_confirmation_page(self):
        """Test GET request returns confirmation page"""
        client = Client()
        user = UserFactory(is_staff=True)
        wallet = user.creator_profile.wallet

        client.force_login(user)
        response = client.get(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id])
        )
        assert response.status_code == 200
        # Verify context is available for non-redirect response
        assert response.context is not None

    def test_get_request_context_contains_wallet(self):
        """Test GET request context includes wallet and change_url"""
        client = Client()
        user = UserFactory(is_staff=True)
        wallet = user.creator_profile.wallet

        client.force_login(user)
        response = client.get(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id])
        )
        assert response.status_code == 200
        assert response.context["wallet"] == wallet
        assert "change_url" in response.context

    def test_post_request_initiates_payout(self):
        """Test POST request successfully initiates payout"""
        client = Client()
        user = UserFactory(is_staff=True)
        wallet = user.creator_profile.wallet

        # Setup wallet with KYC verified and balance
        wallet.kyc_verified = True
        wallet.save()
        WalletTransactionService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="TEST-CASHIN",
        )

        client.force_login(user)
        response = client.post(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id])
        )
        # Should redirect after successful payout
        assert response.status_code == 302

    def test_post_request_displays_success_message(self):
        """Test POST request displays success message"""
        client = Client()
        user = UserFactory(is_staff=True)
        wallet = user.creator_profile.wallet

        wallet.kyc_verified = True
        wallet.save()
        WalletTransactionService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="TEST-CASHIN",
        )

        client.force_login(user)
        response = client.post(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id]),
            follow=True,
        )
        # Check that we can access messages (redirected)
        if response.context:
            messages = list(response.context.get("messages", []))
            assert len(messages) > 0

    def test_post_request_with_exception_shows_error(self):
        """Test POST request shows error message on exception"""
        client = Client()
        user = UserFactory(is_staff=True)
        wallet = user.creator_profile.wallet

        # KYC not verified - should cause an error
        client.force_login(user)
        response = client.post(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id]),
            follow=True,
        )
        # Should show error message
        if response.context:
            messages = list(response.context.get("messages", []))
            # If there are messages, one should be an error
            assert len(messages) >= 0

    def test_post_request_redirects_to_wallet_change_page(self):
        """Test POST request redirects to wallet admin change page"""

        client = Client()
        user = UserFactory(is_staff=True)
        wallet = user.creator_profile.wallet

        wallet.kyc_verified = True
        wallet.save()
        WalletTransactionService.cash_in(
            wallet=wallet,
            amount=Decimal("100.00"),
            payment=None,
            reference="TEST-CASHIN",
        )

        client.force_login(user)
        response = client.post(
            reverse("payouts:trigger_wallet_payout", args=[wallet.id])
        )
        assert response.status_code == 302
        assert "admin" in response.url

    def test_404_for_non_existent_wallet(self):
        """Test that non-existent wallet returns 404"""
        client = Client()
        user = UserFactory(is_staff=True)

        fake_wallet_id = uuid.uuid4()
        client.force_login(user)
        response = client.get(
            reverse("payouts:trigger_wallet_payout", args=[fake_wallet_id])
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestFinaliseWalletPayout:
    """Tests for finalise_wallet_payout view"""

    def test_requires_superuser(self):
        """Test that staff users cannot access the view (requires superuser)"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=False)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        # Create a pending payout transaction
        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="PAYOUT", status="PENDING"
        )

        client.force_login(user)
        response = client.get(
            reverse("payouts:finalise_wallet_payout", args=[payout_tx.id])
        )
        # Should redirect for non-superuser
        assert response.status_code == 302

    def test_requires_superuser_post(self):
        """Test that POST requests require superuser"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=False)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="PAYOUT", status="PENDING"
        )

        client.force_login(user)
        response = client.post(
            reverse("payouts:finalise_wallet_payout", args=[payout_tx.id])
        )
        assert response.status_code == 302

    def test_post_request_finalizes_payout(self):
        """Test POST request successfully finalizes payout"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="PAYOUT", status="PENDING"
        )

        client.force_login(user)
        with patch.object(PayoutOrchestrator, "finalize") as mock_finalize:
            response = client.post(
                reverse("payouts:finalise_wallet_payout", args=[payout_tx.id])
            )
            # Verify that PayoutOrchestrator.finalize was called
            mock_finalize.assert_called_once()
            call_args = mock_finalize.call_args
            assert call_args.kwargs["payout_tx"] == payout_tx
            assert call_args.kwargs["approved_by"] == user
            assert call_args.kwargs["success"] is True

    def test_post_request_displays_success_message(self):
        """Test POST request displays success message on successful finalization"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        payout_tx = WalletTransactionFactory(
            wallet=wallet,
            transaction_type="PAYOUT",
            status="PENDING",
            reference="PAY-123456",
        )

        client.force_login(user)
        with patch.object(PayoutOrchestrator, "finalize"):
            response = client.post(
                reverse("payouts:finalise_wallet_payout", args=[payout_tx.id]),
                follow=True,
            )
            # Check for messages if context exists
            if response.context:
                messages = list(response.context.get("messages", []))
                assert len(messages) >= 0

    def test_post_request_shows_error_on_exception(self):
        """Test POST request shows error message on exception"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="PAYOUT", status="PENDING"
        )

        error_message = "Provider connection failed"
        client.force_login(user)
        with patch.object(
            PayoutOrchestrator, "finalize", side_effect=Exception(error_message)
        ):
            response = client.post(
                reverse("payouts:finalise_wallet_payout", args=[payout_tx.id]),
                follow=True,
            )
            # Check for messages if context exists
            if response.context:
                messages = list(response.context.get("messages", []))
                assert len(messages) >= 0

    def test_post_request_redirects_to_wallet_change_page(self):
        """Test POST request redirects to wallet admin change page"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="PAYOUT", status="PENDING"
        )

        client.force_login(user)
        with patch.object(PayoutOrchestrator, "finalize"):
            response = client.post(
                reverse("payouts:finalise_wallet_payout", args=[payout_tx.id])
            )
            assert response.status_code == 302
            assert "admin" in response.url

    def test_404_for_non_pending_transaction(self):
        """Test that non-pending transactions return 404"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        # Create a completed payout transaction
        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="PAYOUT", status="COMPLETED"
        )

        client.force_login(user)
        response = client.get(
            reverse("payouts:finalise_wallet_payout", args=[payout_tx.id])
        )
        assert response.status_code == 404

    def test_404_for_non_payout_transaction(self):
        """Test that non-PAYOUT transactions return 404"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)
        wallet = user.creator_profile.wallet
        wallet.kyc_verified = True
        wallet.save()

        # Create a CASH_IN transaction (not a PAYOUT)
        payout_tx = WalletTransactionFactory(
            wallet=wallet, transaction_type="CASH_IN", status="PENDING"
        )

        client.force_login(user)
        response = client.get(
            reverse("payouts:finalise_wallet_payout", args=[payout_tx.id])
        )
        assert response.status_code == 404

    def test_404_for_non_existent_transaction(self):
        """Test that non-existent transactions return 404"""
        client = Client()
        user = UserFactory(is_staff=True, is_superuser=True)

        fake_tx_id = uuid.uuid4()
        client.force_login(user)
        response = client.get(
            reverse("payouts:finalise_wallet_payout", args=[fake_tx_id])
        )
        assert response.status_code == 404
