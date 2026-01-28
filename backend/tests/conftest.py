"""
Pytest configuration and fixtures.
"""
import os
import pytest

def pytest_configure():
    """Configure pytest settings."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
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
def creator_profile(db):
    """Fixture for creating a creator profile."""
    from tests.factories import CreatorProfileFactory
    return CreatorProfileFactory()
