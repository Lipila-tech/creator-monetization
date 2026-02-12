"""
Tests for payment-related serializers (Wallet, KYC, Transactions, etc.)
"""
import pytest
from apps.wallets.serializers import (
    WalletListSerializer,
    WalletDetailSerializer,
    WalletUpdateSerializer,
    WalletPayoutAccountSerializer,
    WalletPayoutAccountCreateSerializer,
    WalletTransactionListSerializer,
    WalletTransactionDetailSerializer,
    WalletTransactionCreateSerializer,
    WalletKYCSerializer,
)
pytest.mark.django_db
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
        assert data is not None
        assert data["id"] == str(wallet_transaction_factory.id)
        assert data["amount"] == str(wallet_transaction_factory.amount)
        assert data["transaction_type"] == wallet_transaction_factory.transaction_type
        assert "status" in data

    def test_transaction_list_read_only_fields(self, wallet_txn_factory):
        """Test that all fields are read-only"""
        serializer = WalletTransactionListSerializer(wallet_txn_factory)
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

    def test_serialize_kyc(self, user_factory):
        """Test serialization of KYC"""
        wallet_kyc = user_factory.creator_profile.wallet.kyc
        serializer = WalletKYCSerializer(wallet_kyc)
        data = serializer.data

        assert data["id"] == wallet_kyc.id
        assert data["account_type"] == wallet_kyc.account_type
        assert data["id_document_number"] == wallet_kyc.id_document_number
        assert data["bank_name"] == wallet_kyc.bank_name

    def test_create_kyc_valid(self):
        """Test creating KYC with valid data"""
        data = {
            "id_document_type": "NRC",
            "id_document_number": "123456",
            "account_type": "BANK",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_create_kyc_invalid_document_type(self):
        """Test creating KYC with invalid document type"""
        data = {
            "id_document_type": "INVALID",
            "id_document_number": "123456",
            "account_type": "BANK",
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
            "account_type": "BANK",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert not serializer.is_valid()
        assert "id_document_number" in serializer.errors

    def test_create_kyc_with_invalid_bank(self):
        """Test creating KYC with account bank"""
        data = {
            "id_document_type": "NRC",
            "id_document_number": "123456",
            "account_type": "INVALID_ACCOUNT_TYPE",
            "bank_name": "Standard Chartered",
            "bank_account_name": "John Doe",
            "bank_account_number": "1234567890",
        }
        serializer = WalletKYCSerializer(data=data)
        assert not serializer.is_valid()
        assert "account_type" in serializer.errors
