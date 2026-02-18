from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse
from apps.customauth.models import APIClient
from apps.creators.models import CreatorProfile
from apps.payments.models import Payment, PaymentStatus
from apps.payments.models import PaymentWebhookLog as WebHook
from apps.wallets.models import PaymentAttempt, Refund, Wallet, WalletTransaction

User = get_user_model()


class WebHookAdmin(admin.ModelAdmin):
    list_display = ("payment", "event_type", "status", "processed_at", "external_id")
    list_filter = ("event_type", "status", "processed_at")
    search_fields = ("payment__external_id", "payment__patron_phone")


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
            url = reverse("payouts:finalise_wallet_payout", args=[obj.id])
            return format_html('<a class="button" href="{}">Confirm</a>', url)
        return "-"

    finalize_payout.short_description = "Finalise"


class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "balance", "is_verified", "trigger_payout")

    readonly_fields = ("balance",)

    def save_model(self, request, obj, form, change):
        if change:
            original = Wallet.objects.get(pk=obj.pk)
            obj.balance = original.balance
        super().save_model(request, obj, form, change)

    def trigger_payout(self, obj):
        if obj.balance > 0:
            url = reverse("payouts:trigger_wallet_payout", args=[obj.id])
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
        "status",
        "provider",
        "created_at",
    ]
    list_filter = [
        "status",
        "provider",
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
        "is_successful",
    ]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("reference", "external_id", "status", "provider")},
        ),
        (
            "Payment Details",
            {"fields": ("amount", "currency", "amount_captured", "amount_refunded")},
        ),
        (
            "Customer Information",
            {"fields": ("patron_email", "patron_name")},
        ),
        (
            "Timing",
            {"fields": ("created_at", "updated_at", "completed_at", "captured_at")},
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
            "color: white; padding: 2px 8px; "
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
                    self.message_user(request, f"Captured payment {payment.reference}")
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
    readonly_fields = ["attempt_number", "status", "error_message", "created_at"]
    can_delete = False


class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0
    readonly_fields = ["amount", "currency", "status", "created_at"]
    can_delete = False


class CustomUserAdmin(BaseUserAdmin):
    """Custom admin for CustomUser model."""

    model = User
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "user_type",
        "is_active",
        "is_staff",
        "date_joined",
        "slug",
    )
    list_filter = ("user_type", "is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "updated_at")

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "slug")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("User Type", {"fields": ("user_type",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("date_joined", "updated_at", "last_login")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )


class APIClientAdmin(admin.ModelAdmin):
    """Admin for APIClient model."""

    list_display = ("name", "client_type", "is_active", "rate_limit", "created_at")
    list_filter = ("client_type", "is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("id", "api_key", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name", "description", "id")}),
        ("Configuration", {"fields": ("client_type", "api_key", "rate_limit")}),
        ("Status", {"fields": ("is_active",)}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )

    actions = ["regenerate_api_keys", "deactivate_clients", "activate_clients"]

    def regenerate_api_keys(self, request, queryset):
        """Action to regenerate API keys."""
        for client in queryset:
            client.regenerate_api_key()
        self.message_user(request, f"{queryset.count()} API keys regenerated.")

    regenerate_api_keys.short_description = "Regenerate selected API keys"

    def deactivate_clients(self, request, queryset):
        """Action to deactivate clients."""
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} clients deactivated.")

    deactivate_clients.short_description = "Deactivate selected clients"

    def activate_clients(self, request, queryset):
        """Action to activate clients."""
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} clients activated.")

    activate_clients.short_description = "Activate selected clients"


class CreatorProfileAdmin(admin.ModelAdmin):
    """Admin for CreatorProfile model."""

    list_display = (
        "get_creator_name",
        "status",
        "verified",
        "followers_count",
        "total_earnings",
        "rating",
        "created_at",
    )
    list_filter = ("status", "verified", "created_at")
    search_fields = (
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "followers_count", "total_earnings")

    fieldsets = (
        ("User", {"fields": ("user",)}),
        (
            "Profile Info",
            {"fields": ("bio", "profile_image", "cover_image", "website")},
        ),
        ("Stats", {"fields": ("followers_count", "total_earnings", "rating")}),
        ("Status", {"fields": ("status", "verified")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )

    def get_creator_name(self, obj):
        """Get creator's full name or username."""
        return obj.user.get_full_name() or obj.user.username

    get_creator_name.short_description = "Creator Name"


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(WebHook, WebHookAdmin)
admin.site.register(CreatorProfile, CreatorProfileAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(APIClient, APIClientAdmin)

# Update the admin site header and titles
admin.site.site_header = "TipZed Admin"
admin.site.site_title = "TipZed Admin Portal"
admin.site.index_title = "Welcome to TipZed Admin Portal"
admin.site.site_url = None  # Disable the "View Site" link
