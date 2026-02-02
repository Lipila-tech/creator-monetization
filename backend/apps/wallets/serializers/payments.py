"""
Serializers for Payment model
"""
from rest_framework import serializers
from decimal import Decimal
from django.utils import timezone
from apps.wallets.models.payment import (
    Payment,
    PaymentStatus,
    PaymentProvider,
    PaymentMethod,
    ISPPaymentProvider,
    Currency,
)


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
            "reference",
            "amount",
            "currency",
            "status",
            "status_display",
            "provider",
            "provider_display",
            "payment_method",
            "method_display",
            "patron_email",
            "completed_at",
            "created_at",
        ]
        read_only_fields = fields

    def get_method_display(self, obj):
        if obj.payment_method:
            return obj.get_payment_method_display()
        return None
