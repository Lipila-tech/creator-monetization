"""
Test factories for creating test data.
"""
import factory
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.customauth.models import APIClient
from apps.creators.models import CreatorProfile, CreatorCategory
from apps.payments.models import Payment
from apps.wallets.models import (
    Wallet, WalletKYC, WalletPayoutAccount, WalletTransaction,
    PaymentAttempt, Refund, Dispute, PaymentWebhookLog,)

User = get_user_model()


class CreatorCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreatorCategory

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))
    icon = "tag"
    is_featured = False
    country_code = "ZM"
    is_active = True
    sort_order = 100

class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating test users."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"testuser{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    user_type = "creator"
    is_active = True
    is_staff = False
    is_superuser = False
    slug = factory.LazyAttribute(lambda obj: obj.username.lower())

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """Set password after user creation."""
        if not create:
            return
        password = extracted or "testpass123"
        obj.set_password(password)
        obj.save()


class StaffUserFactory(UserFactory):
    """Factory for creating test staff users."""

    user_type = "staff"
    is_staff = True


class AdminUserFactory(UserFactory):
    """Factory for creating test admin users."""

    user_type = "admin"
    is_staff = True
    is_superuser = True


class APIClientFactory(factory.django.DjangoModelFactory):
    """Factory for creating test API clients."""

    class Meta:
        model = APIClient

    name = factory.Sequence(lambda n: f"Test Client {n}")
    description = factory.Faker("sentence")
    client_type = "web"
    is_active = True
    rate_limit = 1000


class CreatorProfileFactory(factory.django.DjangoModelFactory):
    """Factory for creating test creator profiles."""

    class Meta:
        model = CreatorProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text")
    status = "active"
    followers_count = factory.Faker("random_int", min=0, max=10000)
    total_earnings = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    rating = factory.Faker("pyfloat", min_value=0, max_value=5)
    verified = False
    profile_image = factory.django.ImageField(color='red', format='JPEG')
    cover_image = factory.django.ImageField(color='blue', format='JPEG')
    website = factory.Faker("url")

# ========== WALLET FACTORIES ==========
class WalletFactory(factory.django.DjangoModelFactory):
    """Factory for creating test wallets."""

    class Meta:
        model = Wallet

    creator = factory.SubFactory(CreatorProfileFactory)
    balance = factory.LazyFunction(lambda: Decimal("0.00"))
    currency = "ZMW"
    is_active = True
    kyc_level = "BASIC"
    kyc_verified = False


class WalletPayoutAccountFactory(factory.django.DjangoModelFactory):
    """Factory for creating test wallet payout accounts."""

    class Meta:
        model = WalletPayoutAccount

    wallet = factory.SubFactory(WalletFactory)
    provider = "MTN_MOMO_ZMB"
    phone_number = '0003334455'
    verified = False


class WalletTransactionFactory(factory.django.DjangoModelFactory):
    """Factory for creating test wallet transactions."""

    class Meta:
        model = WalletTransaction

    wallet = factory.SubFactory(WalletFactory)
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, min_value=1)
    fee = factory.Faker("pydecimal", left_digits=3, right_digits=2, min_value=0)
    transaction_type = "CASH_IN"
    status = "PENDING"
    payment = None
    reference = factory.Sequence(lambda n: f"TXN-{n}")
    correlation_id = factory.Sequence(lambda n: f"CORR-{n}")


class WalletKYCFactory(factory.django.DjangoModelFactory):
    """Factory for creating test wallet KYC data."""

    class Meta:
        model = WalletKYC

    wallet = factory.SubFactory(WalletFactory)
    id_document_type = "NRC"
    id_document_number = factory.Sequence(lambda n: f"NRC{n:08d}")
    account_type = factory.Faker("name")
    verified = False
    bank_name = factory.Faker("word")
    bank_account_name = factory.Faker("name")
    bank_account_number = factory.Sequence(lambda n: f"{n:010d}")


# ========== PAYMENT FACTORIES ==========
class PaymentFactory(factory.django.DjangoModelFactory):
    """Factory for creating test payments."""

    class Meta:
        model = Payment

    wallet = factory.SubFactory(WalletFactory)
    reference = factory.Sequence(lambda n: f"PAY-{n:06d}")
    external_id = factory.Sequence(lambda n: f"EXT-{n}")
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, min_value=1)
    currency = "ZMW"
    amount_captured = factory.LazyAttribute(lambda obj: 0)
    amount_refunded = factory.LazyAttribute(lambda obj: 0)
    status = "pending"
    provider = "MTN_MOMO_ZMB"
    patron_email = factory.Faker("email")
    patron_name = factory.Faker("name")
    patron_phone = "0003334455"
    patron_message = "fake message"
    provider_fee = factory.Faker("pydecimal", left_digits=3, right_digits=2, min_value=0)
    net_amount = factory.LazyAttribute(lambda obj: obj.amount - (obj.provider_fee or 0))
    ip_address = factory.Faker("ipv4")
    user_agent = factory.Faker("user_agent")
    risk_score = factory.Faker("pyfloat", min_value=0, max_value=100)
    requires_3ds = False
    redirect_url = factory.Faker("url")
    webhook_url = factory.Faker("url")
    callback_data = factory.Dict({})
    is_deleted = False


class PaymentAttemptFactory(factory.django.DjangoModelFactory):
    """Factory for creating test payment attempts."""

    class Meta:
        model = PaymentAttempt

    payment = factory.SubFactory(PaymentFactory)
    attempt_number = 1
    amount = factory.LazyAttribute(lambda obj: obj.payment.amount)
    currency = "ZMW"
    status = "pending"
    error_code = ""
    error_message = ""
    provider_request = factory.Dict({})
    provider_response = factory.Dict({})
    provider_id = factory.Sequence(lambda n: f"PROV-{n}")
    started_at = factory.Faker("date_time")
    completed_at = None


class RefundFactory(factory.django.DjangoModelFactory):
    """Factory for creating test refunds."""

    class Meta:
        model = Refund

    payment = factory.SubFactory(PaymentFactory)
    amount = factory.LazyAttribute(lambda obj: obj.payment.amount)
    currency = "ZMW"
    reason = factory.Faker("text")
    status = "pending"
    provider = "pawapay"
    external_id = factory.Sequence(lambda n: f"REF-{n}")
    provider_data = factory.Dict({})
    metadata = factory.Dict({})


class DisputeFactory(factory.django.DjangoModelFactory):
    """Factory for creating test disputes."""

    class Meta:
        model = Dispute

    payment = factory.SubFactory(PaymentFactory)
    external_id = factory.Sequence(lambda n: f"DISP-{n}")
    reason = "chargeback"
    status = "needs_response"
    amount = factory.LazyAttribute(lambda obj: obj.payment.amount)
    currency = "ZMW"
    initiated_at = factory.Faker("date_time")
    due_by = factory.Faker("date_time")
    resolved_at = None
    evidence = factory.Dict({})
    communication = factory.Dict({})
    provider = "pawapay"
    provider_data = factory.Dict({})


class PaymentWebhookLogFactory(factory.django.DjangoModelFactory):
    """Factory for creating test payment webhook logs."""

    class Meta:
        model = PaymentWebhookLog

    provider = "pawapay"
    event_type = "deposit.accepted"
    external_id = factory.Sequence(lambda n: f"HOOK-{n}")
    raw_payload = factory.Faker("text")
    parsed_payload = factory.Dict({})
    headers = factory.Dict({"Content-Type": "application/json"})
    status = "received"
    error_message = ""
    payment = factory.SubFactory(PaymentFactory)
    processed_at = None
    processing_time_ms = None
