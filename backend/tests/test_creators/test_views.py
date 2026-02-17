"""
Test cases for creator public views. Used to verify that the views for creators
function as expected.
"""

import io
import pytest
from django.urls import reverse
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from apps.creators.serializers import CreatorPublicSerializer
from tests.factories import UserFactory, CreatorCategoryFactory


@pytest.mark.django_db
class TestUpdateCreatorProfile:
    """Test for updating a creators profile"""

    def test_fail_unauthenticated_request(self, auth_api_client):
        """Test endpoint requires authenticated user"""

        response = auth_api_client.get("/api/v1/creators/profile/me/")

        assert response.status_code == 401

    def test_endpoint_returns_expected_fields(self, auth_api_client, user_factory):
        """Test expected fields are returned"""

        expected_fields = {
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "profile_image",
            "cover_image",
            "website",
            "category_slugs",
        }
        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.get("/api/v1/creators/profile/me/")

        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert set(response.data["data"].keys()) == expected_fields

    def test_get_full_user_profile(
        self, auth_api_client, user_factory, category_factory
    ):
        """Test get prepopulated profile fields"""
        creator_profile = user_factory.creator_profile
        file_obj = io.BytesIO()
        image = Image.new("RGBA", size=(1, 1), color=(255, 0, 0))
        image.save(file_obj, "png")
        file_obj.seek(0)

        fake_profile = SimpleUploadedFile(
            name="test_profile.png", content=file_obj.read(), content_type="image/png"
        )
        file_obj.seek(0)
        fake_cover = SimpleUploadedFile(
            name="test_cover.png", content=file_obj.read(), content_type="image/png"
        )
        original_name = user_factory.first_name
        # Set Personal profile
        user_factory.first_name = "Mwansa"
        user_factory.last_name = "Mwamba"
        user_factory.phone_number = "1112233445"
        user_factory.save()

        # Set creator profile
        creator_profile.profile_image = fake_profile
        creator_profile.cover_image = fake_cover
        creator_profile.categories.set([category_factory.id])
        creator_profile.save()

        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.get("/api/v1/creators/profile/me/")

        assert response.status_code == 200
        data = response.data

        assert data is not None
        assert data["data"]["first_name"] != original_name
        assert data["data"]["first_name"] == "Mwansa"
        assert data["data"]["last_name"] == "Mwamba"
        assert data["data"]["phone_number"] == "1112233445"

        assert data["data"]["category_slugs"][0] == category_factory.slug

    def test_update_partial_user_profile(self, auth_api_client, user_factory):
        """Test Update all required fields except images"""

        data = {
            "first_name": "test",
            "last_name": "surname",
            "bio": "Test bio",
            "phone_number": "09665544",
            "profile_image": '',
            "cover_image": '',
            "categorySlugs": [],
        }
        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.put(
            "/api/v1/creators/profile/me/", data=data)

        assert response.status_code == 200
        assert response.data is not None
        
        assert user_factory.creator_profile.bio == "Test bio"
        
        assert user_factory.first_name == "test"
        assert user_factory.last_name == "surname"
        assert user_factory.phone_number == "09665544"
       
    def test_update_rofile_images(self, auth_api_client, user_factory):
        """Test Update only profile and cover images"""
        creator_profile = user_factory.creator_profile
        file_obj = io.BytesIO()
        image = Image.new("RGBA", size=(1, 1), color=(255, 0, 0))
        image.save(file_obj, "png")
        file_obj.seek(0)
        fake_profile = SimpleUploadedFile(
            name="test_profile.png", content=file_obj.read(), content_type="image/png"
        )
        file_obj.seek(0)
        fake_cover = SimpleUploadedFile(
            name="test_cover.png", content=file_obj.read(), content_type="image/png"
        )
        data = {
            "profile_image": fake_profile,
            "cover_image": fake_cover,
        }
        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.put(
            "/api/v1/creators/profile/me/", data=data, format="multipart"
        )
        assert response.status_code == 200
        assert response.data is not None
        assert creator_profile.profile_image.name is not None
        assert creator_profile.cover_image.name is not None
        assert creator_profile.profile_image.url is not None
        assert creator_profile.cover_image.url is not None

    def test_update_full_user_profile(
        self, auth_api_client, user_factory, category_factory
    ):
        """Test Update all required fields"""
        file_obj = io.BytesIO()
        image = Image.new("RGBA", size=(1, 1), color=(255, 0, 0))
        image.save(file_obj, "png")
        file_obj.seek(0)
        fake_profile = SimpleUploadedFile(
            name="test_profile.png", content=file_obj.read(), content_type="image/png"
        )
        file_obj.seek(0)
        fake_cover = SimpleUploadedFile(
            name="test_cover.png", content=file_obj.read(), content_type="image/png"
        )

        data = {
            "first_name": "test",
            "last_name": "surname",
            "bio": "Test bio",
            "phone_number": "09665544",
            "profile_image": fake_profile,
            "cover_image": fake_cover,
            "website": "https://web.creator.com",
            "category_slugs": [category_factory.slug],
        }
        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.put(
            "/api/v1/creators/profile/me/", data=data, format="multipart"
        )
        # Check user info
        assert response.status_code == 200
        assert response.data is not None
        assert user_factory.first_name == "test"
        # Check categories
        assert (
            user_factory.creator_profile.categories.first().name
            == category_factory.name
        )
        # Check Image update
        creator_profile = user_factory.creator_profile
        assert creator_profile.profile_image.name is not None
        assert creator_profile.cover_image.name is not None
        assert creator_profile.profile_image.url is not None
        assert creator_profile.cover_image.url is not None


    def test_update_user_categories(self, auth_api_client, user_factory):
        categories = CreatorCategoryFactory.create_batch(4)

        c1 = categories[0].slug
        c2 = categories[1].slug
        c3 = categories[2].slug
        c4 = categories[3].slug
       
        data = {
            "category_slugs": [c1, c2, c3, c4]
        }
        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.put(
            "/api/v1/creators/profile/me/", data=data, format="multipart"
        )
        # Check user info
        assert response.status_code == 200

        # Check categories
        assert user_factory.creator_profile.categories.filter() is not None
        assert len(user_factory.creator_profile.categories.filter()) == 4
        

@pytest.mark.django_db
class TestPublicCreatorProfile:
    def test_creator_profile_image_url(self, user_factory):
        """Test that the ImageField in CreatorProfile geenerates a valid URL string"""
        creator_profile = user_factory.creator_profile
        creator_profile.profile_image = "test_images/test_image.png"
        creator_profile.save()

        url = reverse("creators:creator_public_view", args=[creator_profile.user.slug])
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer = CreatorPublicSerializer(creator_profile, context={"request": request})
        data = serializer.data
        expected_url = "http://testserver/media/test_images/test_image.png"
        
        assert data["profile_image"] == expected_url

    def test_list_creator_profiles_view(self, api_client):
        """Test the view that lists all creator profiles."""
        # Create multiple creator profiles
        users = UserFactory.create_batch(3)
        profiles = [user.creator_profile for user in users]

        url = reverse("creators:creator_profiles_list")

        response = api_client.get(url)

        assert response.status_code == 200
        content = response.content.decode()
        for profile in profiles:
            assert profile.user.first_name in content
            assert profile.user.last_name in content
            assert "bio" in content

    def test_creator_public_view(self, api_client, user_factory):
        """Test the public view of a creator profile."""
        creator_profile = user_factory.creator_profile

        url = reverse("creators:creator_public_view", args=[creator_profile.user.slug])

        response = api_client.get(url)

        assert response.status_code == 200
        assert creator_profile.user.first_name in response.content.decode()
        assert creator_profile.user.last_name in response.content.decode()
        assert "bio" in response.content.decode()
        assert "walletId" in response.content.decode()
        assert creator_profile.user.slug in response.content.decode()
        assert creator_profile.user.username in response.content.decode()
        assert creator_profile.website in response.content.decode()
        assert str(creator_profile.followers_count) in response.content.decode()
        assert str(creator_profile.rating) in response.content.decode()
        assert str(creator_profile.verified).lower() in response.content.decode()
        # asert images
        profile_image_url = (
            creator_profile.profile_image.url if creator_profile.profile_image else ""
        )
        cover_image_url = (
            creator_profile.cover_image.url if creator_profile.cover_image else ""
        )
        assert profile_image_url in response.content.decode()
        assert cover_image_url in response.content.decode()

    def test_creator_public_view_not_found(self, api_client):
        """Test that a non-existent creator profile returns 404."""
        url = reverse("creators:creator_public_view", args=["non-existent-slug"])

        response = api_client.get(url)

        assert response.status_code == 404

    def test_creator_public_view_inactive_profile(self, api_client, user_factory):
        """Test that an inactive creator profile returns 404."""
        creator_profile = user_factory.creator_profile
        creator_profile.status = "inactive"
        creator_profile.save()

        url = reverse("creators:creator_public_view", args=[creator_profile.user.slug])

        response = api_client.get(url)

        assert response.status_code == 404

    def test_creator_public_view_content(self, api_client, user_factory):
        """Test that the creator public view displays correct content."""
        creator_profile = user_factory.creator_profile
        creator_profile.bio = "This is a test bio for the creator."
        creator_profile.website = "https://example.com"
        creator_profile.save()

        url = reverse("creators:creator_public_view", args=[creator_profile.user.slug])

        response = api_client.get(url)

        assert response.status_code == 200
        content = response.content.decode()
        assert "This is a test bio for the creator." in content
        assert "https://example.com" in content

    def test_creator_public_view_multiple_profiles(self, api_client):
        """Test that multiple creator profiles can be accessed correctly."""
        users = UserFactory.create_batch(5)
        profiles = [user.creator_profile for user in users]

        for profile in profiles:
            url = reverse("creators:creator_public_view", args=[profile.user.slug])
            response = api_client.get(url)
            assert response.status_code == 200
            assert profile.user.first_name in response.content.decode()
            assert profile.user.last_name in response.content.decode()
            assert "bio" in response.content.decode()

    def test_creator_public_view_slug_case_insensitivity(self, api_client, user_factory):
        """Test that the creator public view is case insensitive regarding slugs."""
        creator_profile = user_factory.creator_profile

        url = reverse(
            "creators:creator_public_view", args=[creator_profile.user.slug.upper()]
        )

        response = api_client.get(url)

        assert response.status_code == 200
        assert creator_profile.user.first_name in response.content.decode()
        assert creator_profile.user.last_name in response.content.decode()
        assert "bio" in response.content.decode()

    def test_creator_public_view_special_characters_in_slug(self, api_client, user_factory):
        """Test that the creator public view handles special characters in slugs."""
        creator_profile = user_factory.creator_profile
        creator_profile.user.slug = "specialchar_slug-123"
        creator_profile.user.save()

        url = reverse("creators:creator_public_view", args=[creator_profile.user.slug])
        response = api_client.get(url)

        assert response.status_code == 200
        assert creator_profile.user.first_name in response.content.decode()
        assert creator_profile.user.last_name in response.content.decode()
        assert "bio" in response.content.decode()

    def test_creator_public_view_redirects(self, api_client, user_factory):
        """Test that the creator public view redirects correctly if needed."""
        creator_profile = user_factory.creator_profile

        url = (
            reverse("creators:creator_public_view", args=[creator_profile.user.slug])
            + "?ref=homepage"
        )

        response = api_client.get(url)

        assert response.status_code == 200
        assert creator_profile.user.first_name in response.content.decode()
        assert creator_profile.user.last_name in response.content.decode()
        assert "bio" in response.content.decode()
