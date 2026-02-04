"""
Serializers for Payment model
"""
from rest_framework import serializers
from .models import Payment

from apps.wallets.models import  Tier


class TierListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(
        source="creator.user.username", read_only=True
    )
    class Meta:
        model = Tier 
        fields = [
            "creator_name",
            "tier_name",
            "amount",
            "tier_type",
            "is_active",
        ]


class PaymentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing payments"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    provider_display = serializers.CharField(
        source="get_provider_display", read_only=True
    )
    method_display = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "wallet",
            "reference",
            "amount",
            "currency",
            "status",
            "isp_provider",
            "payment_method",
            "method_display",
            "patron_phone",
            "patron_email",
            "patron_message",
            "completed_at",
            "created_at",
        ]
        read_only_fields = fields

    def get_method_display(self, obj):
        if obj.payment_method:
            return obj.get_payment_method_display()
        return None


class PaymentSerializer(serializers.ModelSerializer):
    """Lightweight serializer for creating payments"""

    class Meta:
        model = Payment
        fields = [
            "amount",
            "isp_provider",
            "patron_email",
            "patron_phone",
            "patron_message",
        ]
      