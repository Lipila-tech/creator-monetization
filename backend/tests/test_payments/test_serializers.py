"""
Tests for Payment serializers
"""
from apps.payments.serializers import PaymentSerializer

class TestPaymentSerializer:
    """Test PaymentSerializer fields"""

    def test_payment_serializer_fields(self, payment_factory):
        """Test serialization of payment list"""

        expected_fields = {
            'patron_phone', 'patron_email', 'patron_message', 'amount', 'provider','metadata',
        }
        serializer = PaymentSerializer(payment_factory)
        assert set(serializer.data.keys()) == expected_fields