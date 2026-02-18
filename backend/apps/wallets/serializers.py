"""
Serializers for payment-related models (Wallet, WalletTransaction, KYC, etc.)
"""
from rest_framework import serializers
from decimal import Decimal
from django.db import models
from .models import Wallet, WalletPayoutAccount, WalletTransaction, WalletKYC


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
    total_outgoing = serializers.SerializerMethodField()
    # explicitly convert Decimal to string for JSON serialization
    balance = serializers.SerializerMethodField()
    next_payout_date = serializers.SerializerMethodField()

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
            "payout_interval_days",
            "next_payout_date",
            "kyc_level",
            "kyc_verified",
            "transaction_count",
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
            "total_outgoing",
            "created_at",
            "updated_at",
        ]

    def get_transaction_count(self, obj):
        return obj.transactions.count()

    def get_total_outgoing(self, obj):
        return abs(obj.transactions.filter(transaction_type="PAYOUT").aggregate(
            total=models.Sum("amount")
        )["total"] or Decimal("0"))

    def get_next_payout_date(self, obj):
        from .services.wallet_services import PayoutScheduleService
        last_payout = obj.transactions.filter(transaction_type="PAYOUT").order_by("-created_at").first()
        last_payout_date = last_payout.created_at if last_payout else None
        payout_interval = obj.payout_interval_days or 30  # default to 30 days if not set
        next_payout_date = PayoutScheduleService.get_next_payout_date(
            last_payout_date, payout_interval
        )
        return next_payout_date.isoformat() if next_payout_date else None


class WalletUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating wallet"""

    class Meta:
        model = Wallet
        fields = ["is_active", "kyc_level", "payout_interval_days"]

    def validate_kyc_level(self, value):
        """Validate KYC level"""
        valid_levels = ["BASIC", "STANDARD", "ENHANCED"]
        if value not in valid_levels:
            raise serializers.ValidationError(
                f"KYC level must be one of {valid_levels}"
            )
        return value

    def validate_payout_interval_days(self, value):
        """Validate payout interval must be a positive integer and one of the defined choices"""
        if value <= 0:
            raise serializers.ValidationError(
                "Payout interval must be a positive integer"
            )
        valid_intervals = [choice[0] for choice in Wallet.PAYOUT_INTERVAL_CHOICES]
        if value not in valid_intervals:
            raise serializers.ValidationError(
                f"Payout interval must be one of {valid_intervals}"
            )
        return value


# ========== WALLET PAYOUT ACCOUNT SERIALIZERS ==========
class WalletPayoutAccountSerializer(serializers.ModelSerializer):
    """Serializer for wallet payout account"""

    wallet_id = serializers.PrimaryKeyRelatedField(
        source="wallet", read_only=True
    )

    class Meta:
        model = WalletPayoutAccount
        fields = [
            "id",
            "wallet_id",
            "provider",
            "phone_number",
            "account_name",
            "updated_at",
            "verified",
            "created_at",
        ]
        read_only_fields = ["id", "wallet_id", "verified", "created_at", "updated_at"]

    def validate_provider(self, value):
        """Validate provider choice"""
        valid_providers = [p[0] for p in WalletPayoutAccount.PROVIDER_CHOICES]
        if value not in valid_providers:
            raise serializers.ValidationError(
                f"Provider must be one of {valid_providers}"
            )
        return value

    def validate_phone_number(self, value):
        """
        Validate phone number format should be zambian format
        (10 digits, starting with 260)
        """
        if not value or len(value) < 10:
            raise serializers.ValidationError(
                "Phone number must be at least 10 digits"
            )
        if not value.startswith("260"):
            raise serializers.ValidationError(
                "Phone number must start with 260"
            )
        return value

    def update(self, instance, validated_data):
        """
        Override update to prevent changes to wallet and provider fields
        after creation. Only allow updating provider, phone number and account name.
        """
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.account_name = validated_data.get("account_name", instance.account_name)
        instance.provider = validated_data.get("provider", instance.provider)
        instance.save()
        return instance


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
