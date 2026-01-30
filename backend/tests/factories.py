"""
Test factories for creating test data.
"""
import factory
from django.contrib.auth import get_user_model
from apps.customauth.models import APIClient
from apps.creators.models import CreatorProfile

User = get_user_model()


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
    profile_image = None
    cover_image = None
    website = factory.Faker("url")
