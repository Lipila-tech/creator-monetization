"""
Tests for Payment serializers
"""
import pytest
from decimal import Decimal
from apps.payments.serializers import (
    PaymentListSerializer,
)


pytestmark = pytest.mark.django_db

# ========== PAYMENT LIST SERIALIZER TESTS ==========
class TestPaymentListSerializer:
    """Test PaymentListSerializer"""

    def test_serialize_payment_list(self, payment_factory):
        """Test serialization of payment list"""
        serializer = PaymentListSerializer(payment_factory)
        data = serializer.data
        assert data["id"] == str(payment_factory.id)
        assert data["reference"] == payment_factory.reference
        assert data["amount"] == str(payment_factory.amount)
        assert data["currency"] == payment_factory.currency
        assert data["status"] == payment_factory.status
        assert data["provider"] == payment_factory.provider

    def test_payment_list_read_only_fields(self, payment_factory):
        """Test that all fields are read-only"""
        serializer = PaymentListSerializer(payment_factory)
        assert serializer.fields["id"].read_only is True
        assert serializer.fields["reference"].read_only is True
        assert serializer.fields["status"].read_only is True