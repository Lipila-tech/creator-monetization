from django.db import models
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from decimal import Decimal
from typing import Optional, Dict

User = get_user_model()


# ========== ENUMS ==========
class PaymentStatus(models.TextChoices):
    """Payment status enumeration"""

    ACCEPTED = "accepted", _("Accepted")
    PENDING = "pending", _("Pending")
    PROCESSING = "processing", _("Processing")
    COMPLETED = "completed", _("Completed")
    CAPTURED = "captured", _("Captured")
    PARTIALLY_CAPTURED = "partially_captured", _("Partially Captured")
    REFUNDED = "refunded", _("Refunded")
    PARTIALLY_REFUNDED = "partially_refunded", _("Partially Refunded")
    FAILED = "failed", _("Failed")
    CANCELLED = "cancelled", _("Cancelled")
    EXPIRED = "expired", _("Expired")
    REQUIRES_ACTION = "requires_action", _("Requires Action")
    REQUIRES_CONFIRMATION = "requires_confirmation", _("Requires Confirmation")
    DISPUTED = "disputed", _("Disputed")
    IN_RECONCILIATION = "in_reconciliation", _("IN_RECONCILIATION")
    PAID = "paid", _("Paid")
    SUBMITTED = "submitted", _("Submitted")
    REJECTED = "rejected", _("Rejected")


class PaymentMethod(models.TextChoices):
    """Payment method types"""

    CASH = "cash", _("Cash")
    MOBILE_MONEY = "mobile_money", _("Mobile Money")
    CREDIT_CARD = "credit_card", _("Credit Card")


class PaymentProvider(models.TextChoices):
    """Supported payment providers"""

    PAWAPAY = "pawapay", _("Pawapay")
    CUSTOM = "custom", _("custom")
    LIPILA = "lipila", _("Lipila Online")


class PaymentProvider(models.TextChoices):
    """Supported payment providers"""

    MTN_MOMO_ZMB = "MTN_MOMO_ZMB", _("MTN ZAMBIA")
    AIRTEL_MOMO_ZMB = "AIRTEL_OAPI_ZMB", _("AIRTEL MONEY ZAMBIA")
    ZAMTEL_MOMO_ZMB = "ZAMTEL_ZMB", _("ZAMTEL KWACHA")


class Currency(models.TextChoices):
    """ISO 4217 Currency Codes"""

    ZMW = "ZMW", _("Zambian Kwacha")
    EUR = "EUR", _("Euro")
    # Add more as needed


# ========== ABSTRACT BASE MODELS ==========
class TimeStampedModel(models.Model):
    """Abstract base model with created and modified timestamps"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base model with UUID primary key"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Abstract base model for soft deletion"""

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the instance"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """Restore soft deleted instance"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


# ========== PAYMENT MANAGER ===========


class PaymentManager(models.Manager):
    """Custom manager for Payment model with business logic"""

    def get_queryset(self):
        """Override get_queryset to exclude deleted payments by default"""
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        """Get all payments including deleted ones"""
        return super().get_queryset()

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
        """
        Get all successful payments within optional date range
        Args:
            start_date (datetime): Start of date range
            end_date (datetime): End of date range
        Returns:
            QuerySet: Successful payments
        """
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
        """
        Get revenue aggregation by currency within date range
        Aggregates total amount, total fees, and net revenue
        Args:
            start_date (datetime): Start of date range
            end_date (datetime): End of date range
        Returns:
            QuerySet: Aggregated revenue data by currency
        """
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

# ========== MAIN PAYMENT MODEL ==========
class Payment(UUIDModel, TimeStampedModel, SoftDeleteModel):
    """
    Main Payment model with support for multiple gateways,
    currencies, and payment methods
    """

    # Basic Information
    objects = PaymentManager()
    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    reference = models.CharField(
        max_length=100, help_text=_("reference for patron-facing purposes")
    )
    external_id = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        help_text=_("Payment ID from the payment provider"),
    )

    # Payment Details
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text=_("Payment amount in the specified currency"),
    )
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.ZMW
    )
    amount_captured = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Amount successfully captured"),
    )
    amount_refunded = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Amount refunded to patron"),
    )

    # Status and Provider
    status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )
    provider = models.CharField(
        max_length=30,
        choices=PaymentProvider.choices,
        db_index=True,
    )
    patron_phone = models.CharField(
        max_length=12, help_text=_("Zambia standard 10 digit mobile number"))
    patron_email = models.EmailField(
        null=True,
        blank=True,
    )
    patron_name = models.CharField(max_length=255, blank=True, null=True)

    patron_message = models.CharField(
        max_length=100,
        db_index=True,
        null=True,
        blank=True,
    )
    patron_message = models.TextField(blank=True, null=True)
    metadata = models.JSONField(
        default=dict, blank=True, help_text=_("Additional payment metadata")
    )

    # Timing Information
    completed_at = models.DateTimeField(null=True, blank=True)
  
    # Fee and Settlement Information
    provider_fee = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Fee charged by the payment provider"),
    )
    net_amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Amount after provider fees"),
    )
    settled_at = models.DateTimeField(null=True, blank=True)
    settlement_reference = models.CharField(max_length=255, blank=True)

    # Provider-specific fields
    provider_data = models.JSONField(
        default=dict, blank=True, help_text=_(
            "Raw response data from payment provider")
    )
    provider_metadata = models.JSONField(
        default=dict, blank=True, help_text=_(
            "Additional provider-specific metadata")
    )

    # Security and Compliance
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    risk_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text=_("Risk assessment score (0-100)"),
    )
    requires_3ds = models.BooleanField(default=False)

    # Payment Flow
    redirect_url = models.URLField(blank=True)
    webhook_url = models.URLField(blank=True)
    callback_data = models.JSONField(default=dict, blank=True)
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["reference", "status"]),
            models.Index(fields=["patron_phone", "created_at"]),
            models.Index(fields=["created_at", "status"]),
            models.Index(fields=["amount", "currency"]),
        ]
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount_captured__lte=models.F("amount")),
                name="amount_captured_lte_amount",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    amount_refunded__lte=models.F("amount_captured")),
                name="amount_refunded_lte_amount_captured",
            ),
        ]

    def __str__(self):
        return f"{self.reference} - {self.amount}\
            {self.currency} - {self.get_status_display()}"

    def clean(self):
        super().clean()
        if self.amount <= 0:
            raise ValueError("Amount must be at least ZMW30")

    def save(self, *args, **kwargs):
        # Auto-calculate net_amount if provider_fee exists
        if self.provider_fee and self.amount_captured:
            self.net_amount = self.amount_captured - self.provider_fee
        super().save(*args, **kwargs)

    @property
    def amount_remaining(self) -> Decimal:
        """Calculate remaining amount to be captured"""
        return Decimal(self.amount) - Decimal(self.amount_captured)

    
    @property
    def is_successful(self) -> bool:
        """Check if payment was successful"""
        return self.status in [PaymentStatus.CAPTURED, PaymentStatus.COMPLETED]

    
    def update_status(self, new_status: str, metadata: Optional[Dict] = None):
        """Safely update payment status with validation"""
        old_status = self.status
        self.status = new_status

        # Update timestamps based on status changes
        now = timezone.now()

        if (
            new_status == PaymentStatus.COMPLETED
            and old_status != PaymentStatus.ACCEPTED
        ):
            self.completed_at = now
            self.status = PaymentStatus.COMPLETED
        elif (
            new_status == PaymentStatus.CAPTURED
            and old_status != PaymentStatus.CAPTURED
        ):
            self.captured_at = now
            self.status = PaymentStatus.CAPTURED
        elif (
            new_status == PaymentStatus.CANCELLED
            and old_status != PaymentStatus.CANCELLED
        ):
            self.cancelled_at = now
            self.status = PaymentStatus.CANCELLED

        # Update metadata if provided
        if metadata:
            if "metadata" not in self.metadata:
                self.metadata["status_changes"] = []
            self.metadata["status_changes"].append(
                {
                    "from": old_status,
                    "to": new_status,
                    "at": now.isoformat(),
                    "metadata": metadata,
                }
            )
        self.save()

    @classmethod
    def generate_reference(cls, prefix: str = "PAY") -> str:
        """Generate unique payment reference"""
        import secrets
        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = secrets.token_hex(3).upper()
        return f"{prefix}-{timestamp}-{random_str}"
