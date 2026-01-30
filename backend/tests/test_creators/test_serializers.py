import pytest
from tests.factories import CreatorProfileFactory
from apps.creators.serializers import CreatorPublicSerializer, CreatorListSerializer


@pytest.mark.django_db
class TestCreatorPublicSerializer:
    """Test CreatorPublicSerializer."""

    def test_creator_public_serializer(self):
        """Test serialization of creator profile public data."""
        profile = CreatorProfileFactory(bio="This is a test bio.", followers_count=150, rating=4.5)

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user'] == profile.user.id
        assert data['bio'] == "This is a test bio."
        assert data['followers_count'] == 150
        assert data['rating'] == 4.5
        assert 'created_at' in data
        assert 'updated_at' in data
        assert data['website'] == profile.website
        # Remove asset keyword. The utility function itself handles assertions.
        data['profile_image'] == profile.profile_image.url if profile.profile_image else None
        data['cover_image'] == profile.cover_image.url if profile.cover_image else None


    def test_list_creator_public_serializer(self):
        """Test serialization of multiple creator profiles."""
        profiles = [CreatorProfileFactory() for _ in range(3)]

        serializer = CreatorListSerializer(profiles, many=True)
        data = serializer.data

        assert len(data) == 3
        for i in range(3):
            assert data[i]['user'] == profiles[i].user.id
            assert data[i]['bio'] == profiles[i].bio
            assert data[i]['followers_count'] == profiles[i].followers_count
            assert data[i]['rating'] == profiles[i].rating
            assert 'created_at' in data[i]
            assert 'updated_at' in data[i]
            assert data[i]['website'] == profiles[i].website
            
            


    def test_creator_public_serializer_with_verified_profile(self):
        """Test serialization of a verified creator profile."""
        profile = CreatorProfileFactory(verified=True)

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user'] == profile.user.id
        assert data['verified'] is True

    def test_creator_public_serializer_with_inactive_profile(self):
        """Test serialization of an inactive creator profile."""
        profile = CreatorProfileFactory(status="inactive")

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user'] == profile.user.id
        assert data['status'] == "inactive"

    def test_creator_public_serializer_with_suspended_profile(self):
        """Test serialization of a suspended creator profile."""
        profile = CreatorProfileFactory(status="suspended")

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user'] == profile.user.id
        assert data['status'] == "suspended"

    def test_creator_public_serializer_with_banned_profile(self):
        """Test serialization of a banned creator profile."""
        profile = CreatorProfileFactory(status="banned")

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user'] == profile.user.id
        assert data['status'] == "banned"

    def test_creator_public_serializer_edge_case_rating(self):
        """Test serialization of a creator profile with edge case rating values."""
        profile_low = CreatorProfileFactory(rating=0.0)
        profile_high = CreatorProfileFactory(rating=5.0)

        serializer_low = CreatorPublicSerializer(profile_low)
        data_low = serializer_low.data
        assert data_low['rating'] == 0.0

        serializer_high = CreatorPublicSerializer(profile_high)
        data_high = serializer_high.data
        assert data_high['rating'] == 5.0

    def test_creator_public_serializer_no_website(self):
        """Test serialization of a creator profile without a website."""
        profile = CreatorProfileFactory(website="")

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user'] == profile.user.id
        assert data['website'] == ""