"""
Tests for creator profile models.
"""
import pytest
from django.contrib.auth import get_user_model
from apps.creators.models import CreatorProfile
from tests.factories import UserFactory, CreatorProfileFactory

User = get_user_model()


@pytest.mark.django_db
class TestCreatorProfileModel:
    """Test CreatorProfile model."""

    def test_create_creator_profile(self):
        """Test creating a creator profile."""
        profile = CreatorProfileFactory()
        assert profile.user
        assert profile.status == "active"
        assert profile.followers_count >= 0
        assert profile.rating >= 0

    def test_creator_profile_str_representation(self):
        """Test creator profile string representation."""
        user = UserFactory(first_name="John", last_name="Doe")
        profile = CreatorProfileFactory(user=user)
        assert "John Doe" in str(profile)

    def test_is_verified_property(self):
        """Test is_verified property."""
        profile = CreatorProfileFactory(verified=True)
        assert profile.is_verified is True

        profile.verified = False
        assert profile.is_verified is False

    def test_is_suspended_property(self):
        """Test is_suspended property."""
        profile = CreatorProfileFactory(status="suspended")
        assert profile.is_suspended is True

        profile.status = "active"
        assert profile.is_suspended is False

    def test_is_banned_property(self):
        """Test is_banned property."""
        profile = CreatorProfileFactory(status="banned")
        assert profile.is_banned is True

        profile.status = "active"
        assert profile.is_banned is False

    def test_status_choices(self):
        """Test status field choices."""
        for status in ["active", "inactive", "suspended", "banned"]:
            profile = CreatorProfileFactory(status=status)
            assert profile.status == status

    def test_creator_profile_one_to_one(self):
        """Test one-to-one relationship between user and profile."""
        user = UserFactory()
        CreatorProfileFactory(user=user)
        
        # Creating another profile for same user should fail
        with pytest.raises(Exception):
            CreatorProfileFactory(user=user)

    def test_creator_profile_deletion_cascades(self):
        """Test that profile is deleted when user is deleted."""
        user = UserFactory()
        profile = CreatorProfileFactory(user=user)
        profile_id = profile.id
        
        user.delete()
        
        with pytest.raises(CreatorProfile.DoesNotExist):
            CreatorProfile.objects.get(id=profile_id)

    def test_creator_profile_ordering(self):
        """Test creator profiles are ordered by followers count."""
        profile1 = CreatorProfileFactory(followers_count=100)
        profile2 = CreatorProfileFactory(followers_count=500)
        profile3 = CreatorProfileFactory(followers_count=200)
        
        profiles = CreatorProfile.objects.all()
        assert list(profiles) == [profile2, profile3, profile1]
