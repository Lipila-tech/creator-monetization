from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from apps.payments.models import Payment, PaymentStatus


class PaymentManager(models.Manager):
    """Custom manager for Payment model with business logic"""

    def create_payment(self, **kwargs):
        """Create payment with generated reference"""
        if "reference" not in kwargs:
            kwargs["reference"] = Payment.generate_reference()

        payment = self.model(**kwargs)
        payment.full_clean()
        payment.save()
        return payment

    def get_by_reference(self, reference):
        """Get payment by reference"""
        return self.get(reference=reference)

    def get_by_external_id(self, provider, external_id):
        """Get payment by provider and external ID"""
        return self.get(provider=provider, external_id=external_id)

    def get_successful_payments(self, start_date=None, end_date=None):
        """Get all successful payments within date range"""
        queryset = self.filter(
            status__in=[PaymentStatus.CAPTURED, PaymentStatus.COMPLETED],
            is_deleted=False,
        )

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def get_pending_payments(self):
        """Get all pending payments"""
        return self.filter(
            status=PaymentStatus.PENDING,
            is_deleted=False,
            expired_at__gt=timezone.now(),  # Not expired
        )

    def get_failed_payments(self, hours=24):
        """Get failed payments within last N hours"""
        cutoff = timezone.now() - timedelta(hours=hours)
        return self.filter(
            status=PaymentStatus.FAILED,
            is_deleted=False, created_at__gte=cutoff
        )

    def get_revenue_by_currency(self, start_date, end_date):
        """Calculate revenue by currency"""
        return (
            self.get_successful_payments(start_date, end_date)
            .values("currency")
            .annotate(
                total_amount=Sum("amount"),
                total_fees=Sum("provider_fee"),
                net_revenue=Sum("net_amount"),
            )
            .order_by("-total_amount")
        )

    def get_payment_stats(self, start_date, end_date):
        """Get comprehensive payment statistics"""
        queryset = self.filter(
            created_at__range=[start_date, end_date], is_deleted=False
        )

        total = queryset.count()
        successful = queryset.filter(
            status__in=[PaymentStatus.CAPTURED, PaymentStatus.COMPLETED]
        ).count()
        failed = queryset.filter(status=PaymentStatus.FAILED).count()
        refunded = queryset.filter(
            status__in=[
                PaymentStatus.REFUNDED, PaymentStatus.PARTIALLY_REFUNDED]
        ).count()

        # Calculate amounts
        total_amount = queryset.aggregate(
            total=Sum("amount"))["total"] or Decimal("0")

        captured_amount = queryset.filter(
            status__in=[
                PaymentStatus.CAPTURED, PaymentStatus.PARTIALLY_CAPTURED]
        ).aggregate(total=Sum("amount_captured"))["total"] or Decimal("0")

        refunded_amount = queryset.aggregate(total=Sum("amount_refunded"))[
            "total"
        ] or Decimal("0")

        return {
            "total_payments": total,
            "successful_payments": successful,
            "failed_payments": failed,
            "refunded_payments": refunded,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "total_amount": total_amount,
            "captured_amount": captured_amount,
            "refunded_amount": refunded_amount,
            "net_amount": captured_amount - refunded_amount,
        }

    def find_duplicate_payments(
            self, hours=1, amount_tolerance=Decimal("0.01")):
        """Find potential duplicate payments"""
        cutoff = timezone.now() - timedelta(hours=hours)

        # Find payments with same customer,
        # similar amount, and close timestamps
        return (
            self.filter(is_deleted=False, created_at__gte=cutoff)
            .values("customer_email", "currency")
            .annotate(
                count=models.Count("id"),
                total_amount=Sum("amount"),
                min_amount=models.Min("amount"),
                max_amount=models.Max("amount"),
            )
            .filter(
                count__gt=1,
                max_amount__lte=F("min_amount") + amount_tolerance)
        )
