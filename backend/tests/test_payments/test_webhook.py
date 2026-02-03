import json
import uuid
from django.urls import reverse
from decimal import Decimal
import pytest
from apps.payments.models import Payment
from apps.payments.views.cashin import deposit_callback
from apps.wallets.models import WalletTransaction
from apps.payments.services.fee_service import FeeService
from apps.wallets.models import PaymentWebhookLog


class TestDepositCallbackTests:

    @pytest.mark_django_db
    def setup_wallet(self, user_factory):
        wallet = user_factory.creator_profile.wallet
        return wallet

    def test_completed_deposit_credits_wallet(self, api_client, setup_wallet):
        wallet = setup_wallet
        deposit_id = uuid.uuid4()

        Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            provider="pawapay",
            isp_provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=Decimal("10.00"),
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "COMPLETED",
            "amount": "10",
            "providerTransactionId": "ABC123",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 200

        self.wallet.refresh_from_db()
        assert wallet.balance == Decimal("9.70")

    def test_deposit_callback_is_idempotent(self, api_client, setup_wallet):
        wallet = setup_wallet
        deposit_id = uuid.uuid4()

        payment = Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            amount=Decimal("20.00"),
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "COMPLETED",
            "providerTransactionId": "DUPLICATE-TXN",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        deposit_callback(request)
        deposit_callback(request)  # duplicate callback

        self.wallet.refresh_from_db()

        assert wallet.balance == Decimal("19.4")
        assert payment.amount, Decimal("20")
        assert WalletTransaction.objects.filter(
                wallet=wallet, transaction_type="CASH_IN"
            ).count() == 1
        
        assert WalletTransaction.objects.filter(
                wallet=wallet, transaction_type="FEE"
            ).count() == 1
        assert WalletTransaction.objects.filter(
                wallet=wallet, transaction_type="PAYOUT"
            ).count() == 0

    def test_pending_deposit_does_not_credit_wallet(self, api_client, setup_wallet):
        wallet = setup_wallet
        deposit_id = uuid.uuid4()

        Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            amount=Decimal("10.00"),
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "PENDING",
            "providerTransactionId": "PENDING-TXN",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        deposit_callback(request)

        self.wallet.refresh_from_db()
        assert wallet.balance == Decimal("0.00")
        assert WalletTransaction.objects.exists == False

    def test_resend_callback(self,api_client, mocker):
        mock_request = mocker.patch("utils.external_requests.pawapay_request")
        deposit_id = uuid.uuid4()
        mock_request.return_value = (
            {"depositId": str(deposit_id), "status": "COMPLETED"},
            200,
        )

        url = reverse("lipila:deposit_resend", args=[deposit_id])
        response = api_client.get(url)

        assert response.status_code == 200
        assert "data" == response.data

    def test_deposit_callback_updates_payment_completed(self, api_client):
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            provider="pawapay",
            isp_provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=10,
        )

        payload = {
            "depositId": str(deposit_id),
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

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 200

        payment.refresh_from_db()
        assert payment.status == "completed"

        # Check webhook is saved
        webhook = PaymentWebhookLog.objects.all().first()
        assert webhook is not None
        assert webhook.payment == payment
        assert webhook.provider == "pawapay"
        assert webhook.external_id == "ABC123"
        assert webhook.event_type == "deposit.completed"

    def test_deposit_callback_updates_payment_failed(self, api_client):
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            provider="pawapay",
            isp_provider="AIRTEL_OAPI_ZMB",
            customer_phone="260700111222",
            amount=10,
            status="accepted",
        )

        payload = {
            "depositId": str(deposit_id),
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
                "failureMessage": "The customer does not have\
                    enough funds to complete this payment.",
            },
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 200

        payment.refresh_from_db()
        assert payment.status == "failed"

        # Check webhook is saved
        webhook = PaymentWebhookLog.objects.all().first()
        assert webhook is not None
        assert webhook.payment == payment
        assert webhook.provider == "pawapay"
        assert webhook.external_id == "ABC123"
        assert webhook.event_type == "deposit.failed"
        assert "failureCode" in webhook.parsed_payload["failureReason"]
        assert "failureMessage" in webhook.parsed_payload["failureReason"]
        assert webhook.parsed_payload["failureReason"]["failureCode"] == "INSUFFICIENT_BALANCE"

    # ---------------------------------------------------------
    # Test Webhook rejects GET
    # ---------------------------------------------------------
    def test_webhook_rejects_non_post(self, api_client):
        request = api_client(reverse("payments:deposit_callback"))
        response = deposit_callback(request)
        assert response.status_code == 400

    # ---------------------------------------------------------
    # Additional Comprehensive Tests
    # ---------------------------------------------------------

    def test_rejected_deposit_does_not_credit_wallet(self,api_client, setup_wallet):
        """Test that rejected deposits don't credit wallet"""
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            amount=Decimal("50.00"),
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "REJECTED",
            "providerTransactionId": "REJECTED-TXN",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 200

        self.wallet.refresh_from_db()
        assert wallet.balance == Decimal("0.00")
        payment.refresh_from_db()
        assert payment.status == "rejected"

    def test_callback_with_different_isp_providers(self, api_client, setup_wallet):
        """Test callbacks for different ISP providers"""
        wallet = setup_wallet
        providers = ["MTN_MOMO_ZMB", "AIRTEL_OAPI_ZMB", "ZAMTEL_ZMB"]

        for provider in providers:
            deposit_id = uuid.uuid4()
            payment = Payment.objects.create(
                id=deposit_id,
                wallet=wallet,
                provider="pawapay",
                isp_provider=provider,
                customer_phone="260700111222",
                amount=Decimal("10.00"),
            )

            payload = {
                "depositId": str(deposit_id),
                "status": "COMPLETED",
                "providerTransactionId": f"TXN-{provider}",
            }

            request = api_client.post(
                reverse("payments:deposit_callback"),
                data=json.dumps(payload),
                content_type="application/json",
            )

            response = deposit_callback(request)
            assert response.status_code == 200

            payment.refresh_from_db()
            assert payment.status == "completed"

    def test_callback_fee_deduction_accuracy(self, api_client, setup_wallet):
        """Test that fee deduction is accurate for different amounts"""
        test_cases = [
            (Decimal("100.00"), Decimal("97.00")),  # 3% fee = 3
            (Decimal("50.00"), Decimal("48.50")),  # 3% fee = 1.50
            (Decimal("1000.00"), Decimal("970.00")),  # 3% fee = 30
        ]

        for amount, expected_balance in test_cases:
            wallet = setup_wallet

            deposit_id = uuid.uuid4()
            Payment.objects.create(
                id=deposit_id,
                wallet=wallet,
                amount=amount,
            )

            payload = {
                "depositId": str(deposit_id),
                "status": "COMPLETED",
                "providerTransactionId": f"TXN-{amount}",
            }

            request = api_client.post(
                reverse("payments:deposit_callback"),
                data=json.dumps(payload),
                content_type="application/json",
            )

            response = deposit_callback(request)
            assert response.status_code == 200

            wallet.refresh_from_db()
            assert wallet.balance == expected_balance
            # clean up for next iteration
            wallet.delete()

    def test_callback_invalid_json(self, api_client):
        """Test callback with invalid JSON"""
        request = api_client.post(
            reverse("payments:deposit_callback"),
            data="invalid json",
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 400

    def test_callback_missing_deposit_id(self, api_client):
        """Test callback with missing depositId"""
        payload = {
            "status": "COMPLETED",
            "providerTransactionId": "ABC123",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 400

    def test_callback_payment_not_found(self, api_client):
        """Test callback when payment doesn't exist"""
        non_existent_id = uuid.uuid4()
        payload = {
            "depositId": str(non_existent_id),
            "status": "COMPLETED",
            "providerTransactionId": "ABC123",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 404

    def test_callback_without_wallet(self, api_client):
        """Test completed callback for payment without wallet"""
        deposit_id = uuid.uuid4()
        Payment.objects.create(
            id=deposit_id,
            wallet=None,  # No wallet
            amount=Decimal("10.00"),
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "COMPLETED",
            "providerTransactionId": "ABC123",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == [200, 400]

    def test_webhook_logs_all_fields(self, api_client):
        """Test that webhook logs capture all payload fields"""
        deposit_id = uuid.uuid4()
        Payment.objects.create(
            id=deposit_id,
            provider="pawapay",
            amount=100,
        )

        payload = {
            "depositId": str(deposit_id),
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

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 200

        webhook = PaymentWebhookLog.objects.first()
        assert webhook is not None
        assert webhook.parsed_payload["country"] == "ZMB"
        assert webhook.parsed_payload["payer"]["accountDetails"]["provider"] == "MTN_MOMO_ZMB"

    def test_multiple_callbacks_same_payment(self, api_client, setup_wallet):
        """Test multiple callbacks for same payment with different statuses"""
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            amount=Decimal("100.00"),
            status="accepted",
        )

        # First callback - PENDING
        payload_pending = {
            "depositId": str(deposit_id),
            "status": "PENDING",
            "providerTransactionId": "TXN-PENDING",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload_pending),
            content_type="application/json",
        )
        response = deposit_callback(request)
        assert response.status_code == 200

        payment.refresh_from_db()
        assert payment.status == "accepted" # Status remains accepted
        self.wallet.refresh_from_db()
        assert wallet.balance == Decimal("0.00")

        # Second callback - COMPLETED
        payload_completed = {
            "depositId": str(deposit_id),
            "status": "COMPLETED",
            "providerTransactionId": "TXN-COMPLETED",
        }
        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload_completed),
            content_type="application/json",
        )
        response = deposit_callback(request)
        assert response.status_code == 200

        payment.refresh_from_db()
        assert payment.status == "completed"
        self.wallet.refresh_from_db()
        assert wallet.balance == Decimal("97.00")

    def test_callback_with_large_amount(self, api_client, setup_wallet):
        """Test callback with large payment amount"""
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        large_amount = Decimal("999999.99")

        Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            amount=large_amount,
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "COMPLETED",
            "providerTransactionId": "LARGE-TXN",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = deposit_callback(request)
        assert response.status_code == 200

        self.wallet.refresh_from_db()
        # Calculate fee using the same method as the service
        fee = FeeService.calculate_cash_in_fee(large_amount)
        expected_balance = large_amount - fee
        assert wallet.balance == expected_balance

    def test_callback_transaction_atomicity(self, api_client, setup_wallet):
        """Test that callback transaction is atomic"""
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        Payment.objects.create(
            id=deposit_id,
            wallet=wallet,
            amount=Decimal("100.00"),
        )

        payload = {
            "depositId": str(deposit_id),
            "status": "COMPLETED",
            "providerTransactionId": "ATOMIC-TXN",
        }

        request = api_client.post(
            reverse("payments:deposit_callback"),
            data=json.dumps(payload),
            content_type="application/json",
        )

        # Check transactions are created
        initial_tx_count = WalletTransaction.objects.count()
        response = deposit_callback(request)
        final_tx_count = WalletTransaction.objects.count()

        # Should have created CASH_IN and FEE transactions
        assert response.status_code == 200
        assert final_tx_count > initial_tx_count

        # Verify all transactions are consistent
        cash_in_txs = WalletTransaction.objects.filter(
            transaction_type="CASH_IN")
        fee_txs = WalletTransaction.objects.filter(transaction_type="FEE")
        assert cash_in_txs.count() == 1
        assert fee_txs.count() == 1