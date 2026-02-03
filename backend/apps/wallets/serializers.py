"""
Serializers for payment-related models (Wallet, WalletTransaction, KYC, etc.)
"""
from rest_framework import serializers
from decimal import Decimal
from django.db import models
from .models import (
    Wallet,
    WalletPayoutAccount,
    WalletTransaction,
    WalletKYC,
    PaymentAttempt,
    Refund,
    Dispute,
    PaymentWebhookLog,
)


# ========== WALLET SERIALIZERS ==========
class WalletListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing wallets"""

    creator_name = serializers.CharField(
        source="creator.user.get_account_type", read_only=True
    )
    kyc_verified_status = serializers.CharField(
        source="get_kyc_level_display", read_only=True
    )
    # explicitly convert Decimal to string for JSON serialization
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return str(obj.balance)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "creator_name",
            "balance",
            "currency",
            "is_active",
            "kyc_level",
            "kyc_verified_status",
            "kyc_verified",
            "created_at",
        ]
        read_only_fields = fields


class WalletDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single wallet view"""

    creator_id = serializers.PrimaryKeyRelatedField(
        source="creator", read_only=True
    )
    creator_name = serializers.CharField(
        source="creator.user.get_account_type", read_only=True
    )
    transaction_count = serializers.SerializerMethodField()
    total_incoming = serializers.SerializerMethodField()
    total_outgoing = serializers.SerializerMethodField()
     # explicitly convert Decimal to string for JSON serialization
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return str(obj.balance)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "creator_id",
            "creator_name",
            "balance",
            "currency",
            "is_active",
            "kyc_level",
            "kyc_verified",
            "transaction_count",
            "total_incoming",
            "total_outgoing",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "balance",
            "creator_id",
            "creator_name",
            "transaction_count",
            "total_incoming",
            "total_outgoing",
            "created_at",
            "updated_at",
        ]

    def get_transaction_count(self, obj):
        return obj.transactions.count()

    def get_total_incoming(self, obj):
        return obj.transactions.filter(transaction_type="CASH_IN").aggregate(
            total=models.Sum("amount")
        )["total"] or Decimal("0")

    def get_total_outgoing(self, obj):
        return obj.transactions.filter(transaction_type="PAYOUT").aggregate(
            total=models.Sum("amount")
        )["total"] or Decimal("0")


class WalletUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating wallet"""

    class Meta:
        model = Wallet
        fields = ["is_active", "kyc_level"]

    def validate_kyc_level(self, value):
        """Validate KYC level"""
        valid_levels = ["BASIC", "STANDARD", "ENHANCED"]
        if value not in valid_levels:
            raise serializers.ValidationError(
                f"KYC level must be one of {valid_levels}"
            )
        return value


# ========== WALLET PAYOUT ACCOUNT SERIALIZERS ==========
class WalletPayoutAccountSerializer(serializers.ModelSerializer):
    """Serializer for wallet payout account"""

    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )
    wallet_id = serializers.PrimaryKeyRelatedField(
        source="wallet", read_only=True
    )

    class Meta:
        model = WalletPayoutAccount
        fields = [
            "id",
            "wallet_id",
            "provider",
            "provider_display",
            "phone_number",
            "verified",
            "created_at",
        ]
        read_only_fields = ["id", "wallet_id", "verified", "created_at"]

    def validate_provider(self, value):
        """Validate provider choice"""
        valid_providers = [p[0] for p in WalletPayoutAccount.PROVIDER_CHOICES]
        if value not in valid_providers:
            raise serializers.ValidationError(
                f"Provider must be one of {valid_providers}"
            )
        return value

    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value or len(value) < 10:
            raise serializers.ValidationError(
                "Phone number must be at least 10 digits"
            )
        return value


class WalletPayoutAccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payout account"""

    class Meta:
        model = WalletPayoutAccount
        fields = ["provider", "phone_number"]

    def validate_provider(self, value):
        """Validate provider choice"""
        valid_providers = [p[0] for p in WalletPayoutAccount.PROVIDER_CHOICES]
        if value not in valid_providers:
            raise serializers.ValidationError(
                f"Provider must be one of {valid_providers}"
            )
        return value

    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value or len(value) < 10:
            raise serializers.ValidationError(
                "Phone number must be at least 10 digits"
            )
        # Remove non-digit characters for validation
        digits_only = "".join(c for c in value if c.isdigit())
        if len(digits_only) < 10:
            raise serializers.ValidationError(
                "Phone number must contain at least 10 digits"
            )
        return value


# ========== WALLET TRANSACTION SERIALIZERS ==========
class WalletTransactionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing transactions"""

    wallet_id = serializers.PrimaryKeyRelatedField(
        source="wallet", read_only=True
    )
    type_display = serializers.CharField(
        source="get_transaction_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "wallet_id",
            "amount",
            "fee",
            "transaction_type",
            "type_display",
            "status",
            "status_display",
            "reference",
            "created_at",
        ]
        read_only_fields = fields


class WalletTransactionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single transaction view"""

    wallet_id = serializers.PrimaryKeyRelatedField(
        source="wallet", read_only=True
    )
    type_display = serializers.CharField(
        source="get_transaction_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True, allow_null=True
    )
    approved_by_id = serializers.PrimaryKeyRelatedField(
        source="approved_by", read_only=True, allow_null=True
    )
    approved_by_name = serializers.CharField(
        source="approved_by.get_account_type", read_only=True, allow_null=True
    )

    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "wallet_id",
            "amount",
            "fee",
            "transaction_type",
            "type_display",
            "status",
            "status_display",
            "payment_id",
            "reference",
            "correlation_id",
            "approved_by_id",
            "approved_by_name",
            "approved_at",
            "created_at",
        ]
        read_only_fields = fields


class WalletTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating transactions"""

    class Meta:
        model = WalletTransaction
        fields = [
            "amount",
            "fee",
            "transaction_type",
            "correlation_id",
        ]

    def validate_amount(self, value):
        """Validate transaction amount"""
        if value <= Decimal("0"):
            raise serializers.ValidationError(
                "Amount must be greater than 0"
            )
        return value

    def validate_fee(self, value):
        """Validate transaction fee"""
        if value < Decimal("0"):
            raise serializers.ValidationError(
                "Fee cannot be negative"
            )
        return value


# ========== WALLET KYC SERIALIZERS ==========
class WalletKYCSerializer(serializers.ModelSerializer):
    """Serializer for wallet KYC"""

    # convert UUID to string for JSON serialization
    wallet_id = serializers.CharField(
        source="wallet.id", read_only=True
    )
    document_type_display = serializers.CharField(
        source="get_id_document_type_display", read_only=True
    )

    class Meta:
        model = WalletKYC
        fields = [
            "id",
            "wallet_id",
            "id_document_type",
            "document_type_display",
            "id_document_number",
            "account_type",
            "verified",
            "bank_name",
            "bank_account_name",
            "bank_account_number",
            "created_at",
        ]
        read_only_fields = ["id", "wallet_id", "verified", "created_at"]

    def validate_id_document_type(self, value):
        """Validate document type"""
        valid_types = [d[0] for d in WalletKYC.ID_DOCUMENT_TYPE]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Document type must be one of {valid_types}"
            )
        return value

    def validate_id_document_number(self, value):
        """Validate document number format"""
        if not value or len(value) < 3:
            raise serializers.ValidationError(
                "Document number must be at least 3 characters"
            )
        return value

    def validate_account_type(self, value):
        """Validate full name"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Full name must be at least 2 characters"
            )
        return value

    def validate_bank_account_number(self, value):
        """Validate bank account number"""
        if not value or len(value) < 5:
            raise serializers.ValidationError(
                "Bank account number must be at least 5 characters"
            )
        return value


# ========== PAYMENT ATTEMPT SERIALIZERS ==========
class PaymentAttemptSerializer(serializers.ModelSerializer):
    """Serializer for payment attempts"""

    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    currency_display = serializers.CharField(
        source="get_currency_display", read_only=True
    )
    duration = serializers.FloatField(read_only=True)

    class Meta:
        model = PaymentAttempt
        fields = [
            "id",
            "payment_id",
            "attempt_number",
            "amount",
            "currency",
            "currency_display",
            "status",
            "status_display",
            "error_code",
            "error_message",
            "provider_request",
            "provider_response",
            "provider_id",
            "started_at",
            "completed_at",
            "duration",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "payment_id",
            "duration",
            "created_at",
            "updated_at",
        ]


# ========== REFUND SERIALIZERS ==========
class RefundListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing refunds"""

    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )

    class Meta:
        model = Refund
        fields = [
            "id",
            "payment_id",
            "amount",
            "currency",
            "status",
            "status_display",
            "provider",
            "provider_display",
            "created_at",
        ]
        read_only_fields = fields


class RefundDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single refund view"""

    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )

    class Meta:
        model = Refund
        fields = [
            "id",
            "payment_id",
            "amount",
            "currency",
            "reason",
            "status",
            "status_display",
            "provider",
            "provider_display",
            "external_id",
            "provider_data",
            "metadata",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "payment_id",
            "external_id",
            "provider_data",
            "created_at",
            "updated_at",
        ]


# ========== DISPUTE SERIALIZERS ==========
class DisputeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing disputes"""

    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )

    class Meta:
        model = Dispute
        fields = [
            "id",
            "payment_id",
            "external_id",
            "reason",
            "amount",
            "currency",
            "status",
            "status_display",
            "provider",
            "provider_display",
            "initiated_at",
        ]
        read_only_fields = fields


class DisputeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single dispute view"""

    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )

    class Meta:
        model = Dispute
        fields = [
            "id",
            "payment_id",
            "external_id",
            "reason",
            "amount",
            "currency",
            "status",
            "status_display",
            "provider",
            "provider_display",
            "initiated_at",
            "due_by",
            "resolved_at",
            "evidence",
            "communication",
            "provider_data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "payment_id",
            "external_id",
            "provider_data",
            "created_at",
            "updated_at",
        ]


# ========== PAYMENT WEBHOOK LOG SERIALIZERS ==========
class PaymentWebhookLogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing webhook logs"""

    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )
    event_type_display = serializers.CharField(
        source="get_event_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model = PaymentWebhookLog
        fields = [
            "id",
            "provider",
            "provider_display",
            "event_type",
            "event_type_display",
            "status",
            "status_display",
            "external_id",
            "created_at",
        ]
        read_only_fields = fields


class PaymentWebhookLogDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single webhook log view"""

    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )
    event_type_display = serializers.CharField(
        source="get_event_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    payment_id = serializers.PrimaryKeyRelatedField(
        source="payment", read_only=True, allow_null=True
    )

    class Meta:
        model = PaymentWebhookLog
        fields = [
            "id",
            "provider",
            "provider_display",
            "event_type",
            "event_type_display",
            "external_id",
            "raw_payload",
            "parsed_payload",
            "headers",
            "status",
            "status_display",
            "error_message",
            "payment_id",
            "processed_at",
            "processing_time_ms",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
