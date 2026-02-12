import json
import pytest
import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from apps.payments.models import PaymentWebhookLog
from apps.wallets.models import WalletTransaction

User = get_user_model()


@pytest.mark.django_db
class TestPaymentStatusAPIView:
    def test_get_payment_status_pending(
        self, auth_api_client, payment_factory, mocker
    ):
        """Test retrieving payment status with no webhook log"""
        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "COMPLETED"}, 200),
        )
        response = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["status"] == "completed"

        mock_resend.assert_called_once_with(str(payment_factory.id))

    
    def test_get_payment_status_processing(
        self, auth_api_client, payment_factory, mocker
    ):
        """Test retrieving payment status with no webhook log and processing status"""
        payment_factory.status = "processing"
        payment_factory.save()

        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "FAILED"}, 200),
        )
        response = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["status"] == "failed"

        mock_resend.assert_called_once_with(str(payment_factory.id)
    )

    def test_get_payment_status_in_reconciliation(
        self, auth_api_client, payment_factory, mocker
    ):
        """Test retrieving payment status with no webhook log and in_reconciliation status"""
        payment_factory.status = "in_reconciliation"
        payment_factory.save()

        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "COMPLETED"}, 200),
        )
        response = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["status"] == "completed"

        mock_resend.assert_called_once_with(str(payment_factory.id)
    )

    def test_get_payment_status_final_completed(
        self, auth_api_client, payment_factory, mocker
    ):
        """Test retrieving payment status with existing webhook log"""
        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "COMPLETED"}, 200),
        )
        PaymentWebhookLog.objects.create(
            payment=payment_factory,
            provider=payment_factory.provider,
            event_type="deposit.completed",
            external_id="EXT-123",
            parsed_payload={"status": "COMPLETED"},
        )

        payment_factory.status = "completed"
        payment_factory.save()

        response = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["status"] == "completed"

        mock_resend.assert_not_called()

    def test_get_payment_status_with_final_pending(
        self, auth_api_client, payment_factory, mocker
    ):
        """Test retrieving payment status with existing webhook log but pending status"""
        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "FAILED"}, 200),
        )
        PaymentWebhookLog.objects.create(
            payment=payment_factory,
            provider=payment_factory.provider,
            event_type="deposit.pending",
            external_id="EXT-123",
            parsed_payload={"status": "PENDING"},
        )

        payment_factory.status = "PENDING"
        payment_factory.save()

        request = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert request.status_code == 200
        assert request.data["status"] == "failed"
        mock_resend.assert_called_once_with(str(payment_factory.id))

    def test_get_payment_status_final_failed(
        self, auth_api_client, payment_factory, mocker
    ):
        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "COMPLETED"}, 200),
        )

        payment_factory.status = "failed"
        payment_factory.save()

        response = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["status"] == "failed"

        mock_resend.assert_not_called()

    def test_get_payment_status_final_rejected(
        self, auth_api_client, payment_factory, mocker
    ):
        mock_resend = mocker.patch(
            "apps.payments.webhooks.resend_callback",
            return_value=({"status": "COMPLETED"}, 200),
        )

        payment_factory.status = "rejected"
        payment_factory.save()

        response = auth_api_client.get(
            reverse("payments:payment_status", args=[payment_factory.id]), format="json"
        )
        assert response.status_code == 200
        assert response.data["status"] == "rejected"

        mock_resend.assert_not_called()


@pytest.mark.django_db
class TestPaymentWebhookView:

    def test_webhook_credits_wallet_when_payment_is_completed(
        self, api_client, payment_factory
    ):
        """Test that a completed deposit callback credits the wallet
        and records transactions"""
        wallet = payment_factory.wallet

        payload = {
            "depositId": str(payment_factory.id),
            "status": "COMPLETED",
            "amount": payment_factory.amount,
            "providerTransactionId": "ABC123",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )
        assert response.status_code == 200
        wallet.refresh_from_db()
        assert WalletTransaction.objects.filter(
            wallet=wallet, transaction_type="CASH_IN"
        ).exists()
        assert wallet.balance == payment_factory.amount - (
            Decimal("0.1") * payment_factory.amount
        )  # assume 10%
        assert WalletTransaction.objects.filter(
            wallet=wallet, transaction_type="FEE"
        ).exists()
        assert not WalletTransaction.objects.filter(
            wallet=wallet, transaction_type="PAYOUT"
        ).exists()
        assert PaymentWebhookLog.objects.filter(
            payment=payment_factory,
            provider="MTN_MOMO_ZMB",
            external_id="ABC123",
            event_type="deposit.completed",
        ).exists()
        assert PaymentWebhookLog.objects.filter(
            payment=payment_factory,
            provider="MTN_MOMO_ZMB",
            external_id="ABC123",
            event_type="deposit.completed",
        ).first().parsed_payload["amount"] == str(payment_factory.amount)
        assert (
            PaymentWebhookLog.objects.filter(
                payment=payment_factory,
                provider="MTN_MOMO_ZMB",
                external_id="ABC123",
                event_type="deposit.completed",
            )
            .first()
            .parsed_payload["status"]
            == "COMPLETED"
        )
        # Check Wallet Transaction and wallet reference same payment
        cash_in_tx = WalletTransaction.objects.filter(
            wallet=wallet, transaction_type="CASH_IN"
        ).first()
        assert cash_in_tx is not None
        assert cash_in_tx.payment == payment_factory

    def test_webhook_doesnt_credit_wallet_when_payment_is_pending(
        self, api_client, user_factory, payment_factory
    ):
        wallet = user_factory.creator_profile.wallet
        payload = {
            "depositId": str(payment_factory.id),
            "status": "PENDING",
            "providerTransactionId": "PENDING-TXN",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )

        wallet.refresh_from_db()
        assert response.status_code == 200
        assert wallet.balance == Decimal("0.00")
        assert not WalletTransaction.objects.exists()

    def test_webhook_updates_payment_with_final_failed_status(
        self, api_client, payment_factory
    ):
        payload = {
            "depositId": str(payment_factory.id),
            "status": "FAILED",
            "amount": "10",
            "currency": "ZMW",
            "country": "ZMB",
            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "phoneNumber": "260763456789",
                    "provider": "MTN_MOMO_ZMB",
                },
            },
            "created": "2020-02-21T17:32:29Z",
            "customerMessage": "Note of 4 to 22 chars",
            "providerTransactionId": "ABC123",
            "failureReason": {
                "failureCode": "INSUFFICIENT_BALANCE",
                "failureMessage": "The customer does not have enough funds to complete this payment.",
            },
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )
        assert response.status_code == 200

        payment_factory.refresh_from_db()
        assert payment_factory.status == "failed"

        webhook = PaymentWebhookLog.objects.all().first()
        assert webhook is not None
        assert webhook.payment == payment_factory
        assert webhook.provider == "MTN_MOMO_ZMB"
        assert webhook.external_id == "ABC123"
        assert webhook.event_type == "deposit.failed"
        assert "failureCode" in webhook.parsed_payload["failureReason"]
        assert "failureMessage" in webhook.parsed_payload["failureReason"]
        assert (
            webhook.parsed_payload["failureReason"]["failureCode"]
            == "INSUFFICIENT_BALANCE"
        )

    def test_webhook_is_idempotent(self, api_client, payment_factory):
        """Check the endpoint handles duplicate requests correctly"""
        payload = {
            "depositId": str(payment_factory.id),
            "status": "COMPLETED",
            "amount": "10",
            "currency": "ZMW",
            "country": "ZMB",
            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "phoneNumber": "260763456789",
                    "provider": "MTN_MOMO_ZMB",
                },
            },
            "created": "2020-02-21T17:32:29Z",
            "customerMessage": "Note of 4 to 22 chars",
            "providerTransactionId": "ABC123",
        }

        request_payload = json.dumps(payload)

        response1 = api_client.post(
            reverse("payments:webhook"),
            data=request_payload,
            content_type="application/json",
        )
        assert response1.status_code == 200

        payment_factory.refresh_from_db()
        assert payment_factory.status == "completed"

        # Check webhook saved once
        webhooks = PaymentWebhookLog.objects.all()
        assert webhooks.count() == 1

        # duplicate callback
        response2 = api_client.post(
            reverse("payments:webhook"),
            data=request_payload,
            content_type="application/json",
        )
        assert response2.status_code == 200
        assert "Duplicate callback ignored" in response2.content.decode("utf-8")
        assert webhooks.count() == 1
        payment_factory.refresh_from_db()
        assert payment_factory.status == "completed"

    def test_webhook_rejects_non_post_request(self, api_client):
        response = api_client.get(reverse("payments:webhook"))
        assert response.status_code == 405 or response.status_code == 400

    def test_rejected_payment_does_not_credit_wallet(
        self, api_client, user_factory, payment_factory
    ):
        """Test that rejected deposits don't credit wallet"""
        wallet = user_factory.creator_profile.wallet

        payload = {
            "depositId": str(payment_factory.id),
            "status": "REJECTED",
            "providerTransactionId": "REJECTED-TXN",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )
        assert response.status_code == 200

        wallet.refresh_from_db()
        assert wallet.balance == Decimal("0.00")
        payment_factory.refresh_from_db()
        assert payment_factory.status == "rejected"

    def test_webhook_handles_callback_with_invalid_json(self, api_client):
        """Test callback with invalid JSON"""
        response = api_client.post(
            reverse("payments:webhook"),
            data="invalid json",
            content_type="application/json",
        )

        assert response.status_code == 400

    def test_webhook__handles_callback_with_no_payment_id(self, api_client):
        """Test callback with missing depositId"""
        payload = {
            "status": "COMPLETED",
            "providerTransactionId": "ABC123",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )

        assert response.status_code == 400

    def test_webhook_handles_callback_with_no_related_payment(self, api_client):
        """Test callback when payment doesn't exist"""
        non_existent_id = uuid.uuid4()
        payload = {
            "depositId": str(non_existent_id),
            "status": "COMPLETED",
            "providerTransactionId": "ABC123",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )

        assert response.status_code == 404

    def test_webhook_logs_all_fields(self, api_client, payment_factory):
        """Test that webhook logs capture all payload fields"""
        payload = {
            "depositId": str(payment_factory.id),
            "status": "COMPLETED",
            "amount": "100",
            "currency": "ZMW",
            "country": "ZMB",
            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "phoneNumber": "260763456789",
                    "provider": "MTN_MOMO_ZMB",
                },
            },
            "created": "2020-02-21T17:32:29Z",
            "customerMessage": "Test message",
            "providerTransactionId": "EXT-123",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )
        assert response.status_code == 200

        webhook = PaymentWebhookLog.objects.first()
        assert webhook is not None
        assert webhook.parsed_payload["country"] == "ZMB"
        assert (
            webhook.parsed_payload["payer"]["accountDetails"]["provider"]
            == "MTN_MOMO_ZMB"
        )

    def test_multiple_callbacks_same_payment(
        self, api_client, user_factory, payment_factory
    ):
        """Test multiple callbacks for same payment with different statuses"""
        wallet = user_factory.creator_profile.wallet
        payment_factory.status = "accepted"
        payment_factory.save()

        # First callback - PENDING
        payload_pending = {
            "depositId": str(payment_factory.id),
            "status": "PENDING",
            "providerTransactionId": "TXN-PENDING",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            data=json.dumps(payload_pending),
            content_type="application/json",
        )
        assert response.status_code == 200

        payment_factory.refresh_from_db()
        assert (
            payment_factory.status == "accepted"
        )  # status should remain accepted, not overwritten by pending
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("0.00")

        # Second callback - COMPLETED
        payload_completed = {
            "depositId": str(payment_factory.id),
            "status": "COMPLETED",
            "providerTransactionId": "TXN-COMPLETED",
        }
        response = api_client.post(
            reverse("payments:webhook"),
            data=json.dumps(payload_completed),
            content_type="application/json",
        )
        assert response.status_code == 200

        payment_factory.refresh_from_db()
        assert payment_factory.status == "completed"
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("90.00")  # assuming 10% fee on 100 amount

    def test_callback_with_large_amount(
        self, api_client, user_factory, payment_factory
    ):
        """Test callback with large payment amount"""
        from apps.payments.services.fee_service import FeeService

        wallet = user_factory.creator_profile.wallet
        payment_factory.amount = Decimal("999999.99")
        payment_factory.save()

        payload = {
            "depositId": str(payment_factory.id),
            "status": "COMPLETED",
            "providerTransactionId": "LARGE-TXN",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )
        assert response.status_code == 200

        wallet.refresh_from_db()
        fee = FeeService.calculate_cash_in_fee(payment_factory.amount)
        expected_balance = payment_factory.amount - fee
        assert wallet.balance == expected_balance

    def test_callback_with_special_characters_in_message(
        self, api_client, payment_factory
    ):
        """Test callback with special characters in messages"""

        payload = {
            "depositId": str(payment_factory.id),
            "status": "COMPLETED",
            "providerTransactionId": "ABC123",
            "customerMessage": "Payment to creator #123",
        }

        response = api_client.post(
            reverse("payments:webhook"),
            payload,
            content_type="application/json",
        )
        assert response.status_code == 200

        webhook = PaymentWebhookLog.objects.first()
        assert webhook is not None
        assert "Payment to creator #123" in webhook.parsed_payload.get(
            "customerMessage", ""
        )
