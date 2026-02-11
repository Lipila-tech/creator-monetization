import pytest
from tests.factories import UserFactory, CreatorCategoryFactory
from apps.creators.serializers import (
    CreatorPublicSerializer,
    CreatorListSerializer,
    CreatorCategorySerializer,
    UpdateCreatorProfileSerializer)
from apps.creators.models import CreatorCategory
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUpdateCreatorProfileSerializer:

    def test_serializer_update_creator_categories(self, user_factory):

        c1 = CreatorCategoryFactory(name='cat1')
        c2 = CreatorCategoryFactory(name='cat2')
        CreatorCategoryFactory(name='cat3')
        data = {
            'category_slugs': [c1.slug, c2.slug]
        }
        profile = user_factory.creator_profile

        serializer = UpdateCreatorProfileSerializer(
            instance=profile, data=data, partial=True)
        
        assert serializer.is_valid()

        updated_profile = serializer.save()
        assert updated_profile.categories.order_by('id').first().name == 'cat1'
        assert updated_profile.categories.order_by('id').last().name == 'cat2'

    def test_serializer_update_all_wallet_fields(self, user_factory):
        from apps.wallets.models import WalletKYC
        data = {
            'wallet_kyc': {
                "id_document_type": "NRC",
                "id_document_number": "123456",
                "account_type": "BANK",
                "bank_name": "Standard Chartered",
                "bank_account_name": "John Doe",
                "bank_account_number": "1234567890",
            }
        }
        profile = user_factory.creator_profile

        serializer = UpdateCreatorProfileSerializer(
            instance=profile, data=data, partial=True)
        
        assert serializer.is_valid()

        updated_profile = serializer.save()
        wallet = updated_profile.wallet

        wallet_kyc = WalletKYC.objects.get(wallet=wallet)

        assert wallet_kyc.bank_name == "Standard Chartered"
        assert wallet_kyc.bank_account_name  =="John Doe"
        assert wallet_kyc.bank_account_number == "1234567890"


    def test_serializer_update_valid_fields(self, user_factory):
        data = {
            'first_name': 'test', 'last_name': 'surname', 'bio': '',
            'phone_number': '', 'profile_image': None,
            'cover_image': None, 'website': '', 'category_slugs': [], 'wallet_kyc': {}
        }
        profile = user_factory.creator_profile

        serializer = UpdateCreatorProfileSerializer(
            instance=profile, data=data, partial=True)
        assert serializer.is_valid()
        assert serializer.validated_data['first_name'] == "test"
        assert serializer.validated_data['last_name'] == "surname"
        assert serializer.errors == {}

        updated_profile = serializer.save()
        assert updated_profile.user.first_name == 'test'
        assert updated_profile.user.last_name == 'surname'
        assert User.objects.get(id=user_factory.id).first_name == 'test'

    def test_serializer_update_valid_fields_with_missing_fields(self, user_factory):
        data = {
            'first_name': 'test', 'bio': 'My test bio',
        }
        profile = user_factory.creator_profile

        serializer = UpdateCreatorProfileSerializer(
            instance=profile, data=data, partial=True)
        assert serializer.is_valid()
        assert serializer.validated_data['bio'] == "My test bio"

    def test_serializer_fails_update_invalid_fields(self, user_factory):
        data = {
            'first_name': 'test', 'category_slugs': '', 'wallet_kyc': ''
        }
        profile = user_factory.creator_profile

        serializer = UpdateCreatorProfileSerializer(
            instance=profile, data=data, partial=True)
        assert not serializer.is_valid()
        assert 'category_slugs' in serializer.errors
        assert 'wallet_kyc' in serializer.errors

    def test_serializer_update_image_fields(self, user_factory):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile

        file_obj = io.BytesIO()
        image = Image.new("RGBA", size=(1, 1), color=(255, 0, 0))
        image.save(file_obj, 'png')
        file_obj.seek(0)

        fake_profile = SimpleUploadedFile(
            name='test_profile.png',
            content=file_obj.read(),
            content_type='image/png'
        )
        file_obj.seek(0)
        fake_cover = SimpleUploadedFile(
            name='test_cover.png',
            content=file_obj.read(),
            content_type='image/png'
        )
        data = {
            'profile_image': fake_profile, 'cover_image': fake_cover
        }
        profile = user_factory.creator_profile

        serializer = UpdateCreatorProfileSerializer(
            instance=profile, data=data, partial=True)
        assert serializer.is_valid()

        updated_profile = serializer.save()

        assert updated_profile.profile_image is not None
        assert updated_profile.cover_image is not None
        assert updated_profile.profile_image.url is not None
        assert updated_profile.cover_image.url is not None


@pytest.mark.django_db
class TestCreatoryCategorySerializer:
    def test_creator_category_serializer_fields(self, category_factory):
        serializer = CreatorCategorySerializer(category_factory)
        expected_fields = {
            'name', 'slug', 'icon', 'is_featured', 'country_code', 'is_active'
        }
        assert set(serializer.data.keys()) == expected_fields


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
            'created_at', 'updated_at', "wallet_id", "categories"
        }

        assert set(data.keys()) == expected_fields

    def test_creator_public_serializer_contains_categories(self, user_factory):
        """Test serialization of creator profile public data."""
        CreatorCategoryFactory.create_batch(2)
        c1 = CreatorCategory.objects.order_by('id').first()
        c2 = CreatorCategory.objects.order_by('id').last()
        profile = user_factory.creator_profile
        profile.categories.set([c1, c2])

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data
        assert data['categories'] is not None
        assert len(data['categories']) == 2
        assert data['categories'][0]['name'] == c1.name
        assert data['categories'][0]['slug'] == c1.slug
        assert data['categories'][1]['name'] == c2.name
        assert data['categories'][1]['slug'] == c2.slug

    def test_creator_public_serializer(self, user_factory):
        """Test serialization of creator profile public data."""
        profile = user_factory.creator_profile
        profile.bio = "This is a test bio."
        profile.followers_count = 150
        profile.rating = 4.5
        profile.save()

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data
        assert data['wallet_id'] == profile.wallet.id
        assert data['user']["id"] == profile.user.id
        assert data['user']["username"] == profile.user.username
        assert data['user']["first_name"] == profile.user.first_name
        assert data['user']["last_name"] == profile.user.last_name
        assert data['user']["slug"] == profile.user.slug
        assert data['bio'] == "This is a test bio."
        assert data['followers_count'] == 150
        assert data['rating'] == 4.5
        assert data['categories'] == []
        assert 'created_at' in data
        assert 'updated_at' in data
        assert data['website'] == profile.website
        assert data['category'] == profile.user.category
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
            assert data[i]['category'] == profiles[i].category
            assert 'created_at' in data[i]
            assert 'updated_at' in data[i]
            assert 'categories' in data[i]
            assert data[i]['website'] == profiles[i].website

    def test_creator_public_serializer_with_verified_profile(self, user_factory):
        """Test serialization of a verified creator profile."""
        profile = user_factory.creator_profile
        profile.verified = True
        profile.save()

        serializer = CreatorPublicSerializer(profile)
        data = serializer.data

        assert data['wallet_id'] == profile.wallet.id
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
