from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from apps.payments.models import Payment, PaymentStatus
from apps.wallets.models import (
    PaymentAttempt,
    Refund,
    Wallet,
    WalletTransaction,
)
from apps.wallets.models import PaymentWebhookLog as WebHook


class LipilaAdminSite(admin.AdminSite):
    site_header = "Lipila Wallet Administration"
    site_title = "Lipila Wallet Admin"
    index_title = "Welcome to Lipila Wallets Admin"


lipila_admin = LipilaAdminSite(name="lipila_admin")


class WebHookAdmin(admin.ModelAdmin):
    list_display = (
        "payment", "event_type", "status", "processed_at", "external_id")
    list_filter = ("event_type", "status", "processed_at")
    search_fields = ("payment__external_id", "payment__patron_phone")


lipila_admin.register(WebHook, WebHookAdmin)

class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "amount",
        "transaction_type",
        "created_at",
        "status",
        "finalize_payout",
    )

    def finalize_payout(self, obj):
        if (
            obj.amount * -1 > 0
            and obj.transaction_type == "PAYOUT"
            and obj.status == "PENDING"
        ):
            url = reverse("lipila:finalise_wallet_payout", args=[obj.id])
            return format_html('<a class="button" href="{}">Confirm</a>', url)
        return "-"

    finalize_payout.short_description = "Finalise"


lipila_admin.register(WalletTransaction, WalletTransactionAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "balance", "trigger_payout")

    readonly_fields = ("balance",)

    def save_model(self, request, obj, form, change):
        if change:
            original = Wallet.objects.get(pk=obj.pk)
            obj.balance = original.balance
        super().save_model(request, obj, form, change)

    def trigger_payout(self, obj):
        if obj.balance > 0:
            url = reverse("lipila:trigger_wallet_payout", args=[obj.id])
            return format_html('<a class="button" href="{}">Payout</a>', url)
        return "-"

    trigger_payout.short_description = "Payout"


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "reference",
        "external_id",
        "patron_phone",
        "amount",
        "currency",
        "status_badge",
        "provider",
        "isp_provider",
        "created_at",
    ]
    list_filter = [
        "status",
        "isp_provider",
        "payment_method",
        "currency",
        "created_at",
        "is_deleted",
    ]
    search_fields = [
        "external_id",
        "patron_phone",
        "patron_name",
        "order_reference",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "amount_remaining",
        "refundable_amount",
        "is_successful",
        "is_refundable",
    ]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("reference", "external_id", "status", "provider")},
        ),
        (
            "Payment Details",
            {"fields":
             ("amount", "currency", "amount_captured", "amount_refunded")},
        ),
        (
            "Customer Information",
            {"fields": ("patron_email", "patron_name")},
        ),
        (
            "Timing",
            {"fields": (
                "created_at", "updated_at", "completed_at", "captured_at")},
        ),
        (
            "Metadata",
            {
                "fields": ("metadata", "provider_data", "provider_metadata"),
                "classes": ("collapse",),
            },
        ),
    )

    def status_badge(self, obj):
        colors = {
            "pending": "gray",
            "processing": "blue",
            "captured": "green",
            "failed": "red",
            "refunded": "orange",
        }
        color = colors.get(obj.status, "gray")
        return format_html(
            '<span style="background-color: {};'
            'color: white; padding: 2px 8px; '
            'border-radius: 10px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_deleted=False)
        return qs

    actions = ["capture_payments", "refund_payments", "mark_as_deleted"]

    def capture_payments(self, request, queryset):
        for payment in queryset:
            if payment.status in [
                PaymentStatus.COMPLETED,
                PaymentStatus.PARTIALLY_CAPTURED,
            ]:
                try:
                    payment.capture()
                    self.message_user(
                        request, f"Captured payment {payment.reference}")
                except Exception as e:
                    self.message_user(
                        request,
                        f"Failed to capture {payment.reference}: {str(e)}",
                        level="error",
                    )

    capture_payments.short_description = "Capture selected payments"

    def mark_as_deleted(self, request, queryset):
        count = queryset.update(is_deleted=True)
        self.message_user(request, f"Marked {count} payments as deleted")

    mark_as_deleted.short_description = "Soft delete selected payments"

class PaymentAttemptInline(admin.TabularInline):
    model = PaymentAttempt
    extra = 0
    readonly_fields = [
        "attempt_number", "status", "error_message", "created_at"
        ]
    can_delete = False


class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0
    readonly_fields = ["amount", "currency", "status", "created_at"]
    can_delete = False


lipila_admin.register(Wallet, WalletAdmin)
lipila_admin.register(Payment, PaymentAdmin)
