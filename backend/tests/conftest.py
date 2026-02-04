"""
Pytest configuration and fixtures.
"""
import os
import pytest
from decimal import Decimal
from apps.payments.models import PaymentStatus
from apps.payments.models import (
    PaymentStatus,
    PaymentProvider,
    Currency,
)
from apps.wallets.models import WalletTransaction as WTxn
def pytest_configure():
    """Configure pytest settings."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    import django
    django.setup()


@pytest.fixture
def api_client():
    """Fixture for DRF API client."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def rf():
    """Fixture for Django request factory."""
    from django.test import RequestFactory
    return RequestFactory()


@pytest.fixture
def admin_user(db):
    """Fixture for creating an admin user."""
    from tests.factories import AdminUserFactory
    return AdminUserFactory()


@pytest.fixture
def staff_user(db):
    """Fixture for creating a staff user."""
    from tests.factories import StaffUserFactory
    return StaffUserFactory()


@pytest.fixture
def creator_user(db):
    """Fixture for creating a creator user."""
    from tests.factories import UserFactory
    return UserFactory(user_type='creator')


@pytest.fixture
def api_client_obj(db):
    """Fixture for creating an API client."""
    from tests.factories import APIClientFactory
    return APIClientFactory()


@pytest.fixture
def user_factory(db):
    """Create a test user"""
    from tests.factories import UserFactory
    return UserFactory()


@pytest.fixture
def payment_factory(user_factory):
    """Create a test payment"""
    from tests.factories import PaymentFactory
    return PaymentFactory(
        wallet=user_factory.creator_profile.wallet,
        amount=Decimal("100.00"),
        currency=Currency.ZMW,
        status=PaymentStatus.PENDING,
        provider=PaymentProvider.PAWAPAY,
    )


@pytest.fixture
def payout_account_factory(user_factory):
    """Create a test payout account"""
    from tests.factories import WalletPayoutAccountFactory
    return WalletPayoutAccountFactory(wallet=user_factory.creator_profile.wallet)

@pytest.fixture
def wallet_txn_factory(user_factory, payment_factory):
    """Create a test wallet transaction"""
    from tests.factories import WalletTransactionFactory as WalletTxn
    def create_txn(**kwargs):
        defaults = {
            "wallet":user_factory.creator_profile.wallet,
            "amount":0,
            "payment": payment_factory,
            "status": "PENDING"
            }
        defaults.update(kwargs)
        instance = WalletTxn(**defaults)
        return instance
    yield create_txn

@pytest.fixture
def wallet_transaction_factory(user_factory, payment_factory):
    from tests.factories import WalletTransactionFactory
    return WalletTransactionFactory(
        wallet=user_factory.creator_profile.wallet,
        payment=payment_factory
    )

@pytest.fixture
def txn_filter(db):
    """Factory that filter for existing transactions"""
    def _find(**filters):
        """Filter for existing data"""
        return WTxn.objects.filter(**filters).first()
    return _find

@pytest.fixture
def wallet_kyc_factory(user_factory):
    """Create a test wallet KYC"""
    from tests.factories import WalletKYCFactory
    return WalletKYCFactory(wallet=user_factory.creator_profile.wallet)


@pytest.fixture
def payment_attempt_factory(payment_factory):
    """Create a test payment attempt"""
    from tests.factories import PaymentAttemptFactory
    return PaymentAttemptFactory(payment=payment_factory)


@pytest.fixture
def refund_factory(payment_factory):
    """Create a test refund"""
    from tests.factories import RefundFactory
    return RefundFactory(payment=payment_factory)


@pytest.fixture
def dispute_factory(payment_factory):
    """Create a test dispute"""
    from tests.factories import DisputeFactory
    return DisputeFactory(payment=payment_factory)


@pytest.fixture
def webhook_log_factory(payment_factory):
    """Create a test webhook log"""
    from tests.factories import PaymentWebhookLogFactory
    return PaymentWebhookLogFactory(payment=payment_factory)

