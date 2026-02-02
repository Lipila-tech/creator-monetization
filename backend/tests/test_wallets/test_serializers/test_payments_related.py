"""
Tests for payment-related serializers (Wallet, KYC, Transactions, etc.)
"""
import pytest
from apps.wallets.serializers.payments_related import (
    WalletListSerializer,
    WalletDetailSerializer,
    WalletUpdateSerializer,
    WalletPayoutAccountSerializer,
    WalletPayoutAccountCreateSerializer,
    WalletTransactionListSerializer,
    WalletTransactionDetailSerializer,
    WalletTransactionCreateSerializer,
    WalletKYCSerializer,
    PaymentAttemptSerializer,
    RefundListSerializer,
    RefundDetailSerializer,
    DisputeListSerializer,
    DisputeDetailSerializer,
    PaymentWebhookLogListSerializer,
    PaymentWebhookLogDetailSerializer,
)
from tests.factories import (UserFactory)
pytestmark = pytest.mark.django_db

# ========== WALLET SERIALIZER TESTS ==========
class TestWalletListSerializer:
    """Test WalletListSerializer"""
    
    def test_serialize_wallet_list(self, user_factory):
        """Test serialization of wallet list"""
        wallet_factory = user_factory.creator_profile.wallet
        serializer = WalletListSerializer(wallet_factory)
        data = serializer.data

        assert data["id"] == str(wallet_factory.id)
        assert data["balance"] == str(wallet_factory.balance)
        assert data["currency"] == wallet_factory.currency
        assert data["is_active"] is True

    def test_wallet_list_read_only_fields(self, user_factory):
        wallet_factory = user_factory.creator_profile.wallet

        """Test that all fields are read-only"""
        serializer = WalletListSerializer(wallet_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["balance"].read_only is True


class TestWalletDetailSerializer:
    """Test WalletDetailSerializer"""

    def test_serialize_wallet_detail(self, user_factory):
        """Test detailed serialization of wallet"""
        wallet_factory = user_factory.creator_profile.wallet
        serializer = WalletDetailSerializer(wallet_factory)
        data = serializer.data

        assert data["id"] == str(wallet_factory.id)
        assert data["balance"] == str(wallet_factory.balance)
        assert data["currency"] == wallet_factory.currency
        assert "transaction_count" in data

    def test_wallet_detail_computed_fields(self, user_factory):
        """Test computed fields in detail serializer"""
        wallet_factory = user_factory.creator_profile.wallet
        serializer = WalletDetailSerializer(wallet_factory)
        data = serializer.data

        assert "transaction_count" in data
        assert "total_incoming" in data
        assert "total_outgoing" in data


class TestWalletUpdateSerializer:
    """Test WalletUpdateSerializer"""

    def test_update_wallet_is_active(self, user_factory):
        """Test updating wallet is_active field"""
        wallet_factory = user_factory.creator_profile.wallet
        data = {"is_active": False}
        serializer = WalletUpdateSerializer(wallet_factory, data=data, partial=True)
        assert serializer.is_valid(), serializer.errors

    def test_update_wallet_kyc_level(self, user_factory):
        """Test updating wallet KYC level"""
        wallet_factory = user_factory.creator_profile.wallet
        data = {"kyc_level": "STANDARD"}
        serializer = WalletUpdateSerializer(wallet_factory, data=data, partial=True)
        assert serializer.is_valid(), serializer.errors

    def test_update_wallet_invalid_kyc_level(self, user_factory):
        """Test updating with invalid KYC level"""
        wallet_factory = user_factory.creator_profile.wallet
        data = {"kyc_level": "INVALID"}
        serializer = WalletUpdateSerializer(wallet_factory, data=data, partial=True)
        assert not serializer.is_valid()
        assert "kyc_level" in serializer.errors


# ========== WALLET PAYOUT ACCOUNT SERIALIZER TESTS ==========
class TestWalletPayoutAccountSerializer:
    """Test WalletPayoutAccountSerializer"""

    def test_serialize_payout_account(self, payout_account_factory):
        """Test serialization of payout account"""
        serializer = WalletPayoutAccountSerializer(payout_account_factory)
        data = serializer.data

        assert data["provider"] == payout_account_factory.provider
        assert data["phone_number"] == payout_account_factory.phone_number
        assert "id" in data
        assert "wallet_id" in data

    def test_payout_account_read_only_fields(self, payout_account_factory):
        """Test read-only fields"""
        serializer = WalletPayoutAccountSerializer(payout_account_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["verified"].read_only is True


class TestWalletPayoutAccountCreateSerializer:
    """Test WalletPayoutAccountCreateSerializer"""

    def test_create_payout_account_valid(self):
        """Test creating payout account with valid data"""
        data = {
            "provider": "MTN_MOMO_ZMB",
            "phone_number": "260960123456",
        }
        serializer = WalletPayoutAccountCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_create_payout_account_invalid_provider(self):
        """Test creating with invalid provider"""
        data = {
            "provider": "INVALID_PROVIDER",
            "phone_number": "260960123456",
        }
        serializer = WalletPayoutAccountCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "provider" in serializer.errors

    def test_create_payout_account_short_phone(self):
        """Test creating with short phone number"""
        data = {
            "provider": "MTN_MOMO_ZMB",
            "phone_number": "12345",
        }
        serializer = WalletPayoutAccountCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "phone_number" in serializer.errors


# ========== WALLET TRANSACTION SERIALIZER TESTS ==========
class TestWalletTransactionListSerializer:
    """Test WalletTransactionListSerializer"""

    def test_serialize_transaction_list(self, wallet_transaction_factory):
        """Test serialization of transaction list"""
        serializer = WalletTransactionListSerializer(wallet_transaction_factory)
        data = serializer.data

        assert data["id"] == str(wallet_transaction_factory.id)
        assert data["amount"] == str(wallet_transaction_factory.amount)
        assert data["transaction_type"] == wallet_transaction_factory.transaction_type
        assert "status" in data

    def test_transaction_list_read_only_fields(self, wallet_transaction_factory):
        """Test that all fields are read-only"""
        serializer = WalletTransactionListSerializer(wallet_transaction_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["status"].read_only is True


class TestWalletTransactionDetailSerializer:
    """Test WalletTransactionDetailSerializer"""

    def test_serialize_transaction_detail(self, wallet_transaction_factory):
        """Test detailed serialization of transaction"""
        serializer = WalletTransactionDetailSerializer(wallet_transaction_factory)
        data = serializer.data

        assert data["id"] == str(wallet_transaction_factory.id)
        assert data["amount"] == str(wallet_transaction_factory.amount)
        assert "correlation_id" in data
        assert "reference" in data


class TestWalletTransactionCreateSerializer:
    """Test WalletTransactionCreateSerializer"""

    def test_create_transaction_valid(self):
        """Test creating transaction with valid data"""
        data = {
            "amount": "50.00",
            "fee": "2.50",
            "transaction_type": "CASH_IN",
            "correlation_id": "corr_12345",
        }
        serializer = WalletTransactionCreateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_create_transaction_zero_amount(self):
        """Test creating transaction with zero amount"""
        data = {
            "amount": "0.00",
            "fee": "0.00",
            "transaction_type": "CASH_IN",
            "correlation_id": "corr_12345",
        }
        serializer = WalletTransactionCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors

    def test_create_transaction_negative_amount(self):
        """Test creating transaction with negative amount"""
        data = {
            "amount": "-50.00",
            "fee": "0.00",
            "transaction_type": "CASH_IN",
            "correlation_id": "corr_12345",
        }
        serializer = WalletTransactionCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors

    def test_create_transaction_negative_fee(self):
        """Test creating transaction with negative fee"""
        data = {
            "amount": "50.00",
            "fee": "-2.50",
            "transaction_type": "CASH_IN",
            "correlation_id": "corr_12345",
        }
        serializer = WalletTransactionCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "fee" in serializer.errors


# ========== WALLET KYC SERIALIZER TESTS ==========
class TestWalletKYCSerializer:
    """Test WalletKYCSerializer"""

    def test_serialize_kyc(self, wallet_kyc_factory):
        """Test serialization of KYC"""
        serializer = WalletKYCSerializer(wallet_kyc_factory)
        data = serializer.data

        assert data["id"] == wallet_kyc_factory.id
        assert data["full_name"] == wallet_kyc_factory.full_name
        assert data["id_document_number"] == wallet_kyc_factory.id_document_number
        assert data["bank_name"] == wallet_kyc_factory.bank_name

    def test_create_kyc_valid(self, user_factory):
        """Test creating KYC with valid data"""
        data = {
            "id_document_type": "NRC",
            "id_document_number": "123456",
            "full_name": "John Doe",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_create_kyc_invalid_document_type(self, user_factory):
        """Test creating KYC with invalid document type"""
        data = {
            "id_document_type": "INVALID",
            "id_document_number": "123456",
            "full_name": "John Doe",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert not serializer.is_valid()
        assert "id_document_type" in serializer.errors

    def test_create_kyc_short_document_number(self):
        """Test creating KYC with short document number"""
        data = {
            "id_document_type": "NRC",
            "id_document_number": "12",
            "full_name": "John Doe",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert not serializer.is_valid()
        assert "id_document_number" in serializer.errors

    def test_create_kyc_short_full_name(self):
        """Test creating KYC with short full name"""
        data = {
            "id_document_type": "NRC",
            "id_document_number": "123456",
            "full_name": "J",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert not serializer.is_valid()
        assert "full_name" in serializer.errors


# ========== PAYMENT ATTEMPT SERIALIZER TESTS ==========
class TestPaymentAttemptSerializer:
    """Test PaymentAttemptSerializer"""

    def test_serialize_payment_attempt(self, payment_attempt_factory):
        """Test serialization of payment attempt"""
        serializer = PaymentAttemptSerializer(payment_attempt_factory)
        data = serializer.data

        assert data["id"] == str(payment_attempt_factory.id)
        assert data["attempt_number"] == payment_attempt_factory.attempt_number
        assert data["amount"] == str(payment_attempt_factory.amount)
        assert data["status"] == payment_attempt_factory.status

    def test_payment_attempt_read_only_fields(self, payment_attempt_factory):
        """Test read-only fields"""
        serializer = PaymentAttemptSerializer(payment_attempt_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["payment_id"].read_only is True
        assert serializer.fields["duration"].read_only is True


# ========== REFUND SERIALIZER TESTS ==========
class TestRefundListSerializer:
    """Test RefundListSerializer"""

    def test_serialize_refund_list(self, refund_factory):
        """Test serialization of refund list"""
        serializer = RefundListSerializer(refund_factory)
        data = serializer.data

        assert data["id"] == str(refund_factory.id)
        assert data["amount"] == str(refund_factory.amount)
        assert data["currency"] == refund_factory.currency
        assert data["status"] == refund_factory.status

    def test_refund_list_read_only_fields(self, refund_factory):
        """Test that all fields are read-only"""
        serializer = RefundListSerializer(refund_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["payment_id"].read_only is True


class TestRefundDetailSerializer:
    """Test RefundDetailSerializer"""

    def test_serialize_refund_detail(self, refund_factory):
        """Test detailed serialization of refund"""
        serializer = RefundDetailSerializer(refund_factory)
        data = serializer.data

        assert data["id"] == str(refund_factory.id)
        assert data["amount"] == str(refund_factory.amount)
        assert "reason" in data
        assert "provider" in data


# ========== DISPUTE SERIALIZER TESTS ==========
class TestDisputeListSerializer:
    """Test DisputeListSerializer"""

    def test_serialize_dispute_list(self, dispute_factory):
        """Test serialization of dispute list"""
        serializer = DisputeListSerializer(dispute_factory)
        data = serializer.data

        assert data["id"] == str(dispute_factory.id)
        assert data["external_id"] == dispute_factory.external_id
        assert data["reason"] == dispute_factory.reason
        assert data["status"] == dispute_factory.status

    def test_dispute_list_read_only_fields(self, dispute_factory):
        """Test that all fields are read-only"""
        serializer = DisputeListSerializer(dispute_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["payment_id"].read_only is True


class TestDisputeDetailSerializer:
    """Test DisputeDetailSerializer"""

    def test_serialize_dispute_detail(self, dispute_factory):
        """Test detailed serialization of dispute"""
        serializer = DisputeDetailSerializer(dispute_factory)
        data = serializer.data

        assert data["id"] == str(dispute_factory.id)
        assert data["external_id"] == dispute_factory.external_id
        assert "evidence" in data
        assert "communication" in data


# ========== WEBHOOK LOG SERIALIZER TESTS ==========
class TestPaymentWebhookLogListSerializer:
    """Test PaymentWebhookLogListSerializer"""

    def test_serialize_webhook_log_list(self, webhook_log_factory):
        """Test serialization of webhook log list"""
        serializer = PaymentWebhookLogListSerializer(webhook_log_factory)
        data = serializer.data

        assert data["id"] == str(webhook_log_factory.id)
        assert data["provider"] == webhook_log_factory.provider
        assert data["event_type"] == webhook_log_factory.event_type
        assert data["status"] == webhook_log_factory.status

    def test_webhook_log_list_read_only_fields(self, webhook_log_factory):
        """Test that all fields are read-only"""
        serializer = PaymentWebhookLogListSerializer(webhook_log_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["provider"].read_only is True


class TestPaymentWebhookLogDetailSerializer:
    """Test PaymentWebhookLogDetailSerializer"""

    def test_serialize_webhook_log_detail(self, webhook_log_factory):
        """Test detailed serialization of webhook log"""
        serializer = PaymentWebhookLogDetailSerializer(webhook_log_factory)
        data = serializer.data

        assert data["id"] == str(webhook_log_factory.id)
        assert data["provider"] == webhook_log_factory.provider
        assert data["event_type"] == webhook_log_factory.event_type
        assert "raw_payload" in data
        assert "parsed_payload" in data
