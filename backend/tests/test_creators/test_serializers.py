import pytest
from tests.factories import UserFactory
from apps.creators.serializers import CreatorPublicSerializer, CreatorListSerializer


@pytest.mark.django_db
class TestCreatorPublicSerializer:
    """Test CreatorPublicSerializer."""

    def test_creator_serializer_fields(self, user_factory):
        """Test that the serializer includes all expected fields."""
        profile = user_factory.creator_profile

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        expected_fields = {
            'user', 'bio', 'profile_image', 'cover_image', 'website',
            'followers_count', 'rating', 'verified', 'status',
            'created_at', 'updated_at'
        }

        assert set(data.keys()) == expected_fields
        

    def test_creator_public_serializer(self, user_factory):
        """Test serialization of creator profile public data."""
        profile = user_factory.creator_profile
        profile.bio = "This is a test bio."
        profile.followers_count = 150
        profile.rating = 4.5
        profile.save()
        
        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user']["id"] == profile.user.id
        assert data['user']["username"] == profile.user.username
        assert data['user']["first_name"] == profile.user.first_name
        assert data['user']["last_name"] == profile.user.last_name
        assert data['user']["slug"] == profile.user.slug
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
        users = UserFactory.create_batch(3)
        profiles = [user.creator_profile for user in users]

        serializer = CreatorListSerializer(profiles, many=True)
        data = serializer.data

        assert len(data) == 3
        for i in range(3):
            assert data[i]['user']["id"] == profiles[i].user.id
            assert data[i]['user']["username"] == profiles[i].user.username
            assert data[i]['user']["first_name"] == profiles[i].user.first_name
            assert data[i]['user']["last_name"] == profiles[i].user.last_name
            assert data[i]['user']["slug"] == profiles[i].user.slug
            assert data[i]['bio'] == profiles[i].bio
            assert data[i]['followers_count'] == profiles[i].followers_count
            assert data[i]['rating'] == profiles[i].rating
            assert 'created_at' in data[i]
            assert 'updated_at' in data[i]
            assert data[i]['website'] == profiles[i].website
            
            


    def test_creator_public_serializer_with_verified_profile(self, user_factory):
        """Test serialization of a verified creator profile."""
        profile = user_factory.creator_profile
        profile.verified = True
        profile.save()

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user']["id"] == profile.user.id
        assert data['verified'] is True

    def test_creator_public_serializer_with_inactive_profile(self, user_factory):
        """Test serialization of an inactive creator profile."""
        profile = user_factory.creator_profile
        profile.status = "inactive"
        profile.save()

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user']["id"] == profile.user.id
        assert data['status'] == "inactive"

    def test_creator_public_serializer_with_suspended_profile(self, user_factory):
        """Test serialization of a suspended creator profile."""
        profile = user_factory.creator_profile
        profile.status = "suspended"
        profile.save()

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['user']["id"] == profile.user.id
        assert data['status'] == "suspended"
