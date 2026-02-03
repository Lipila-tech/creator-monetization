"""
Test cases for creator public views. Used to verify that the views for creators
function as expected.
"""
import pytest
from django.urls import reverse
from tests.factories import CreatorProfileFactory, UserFactory

@pytest.mark.django_db
def test_list_creator_profiles_view(client):
    """Test the view that lists all creator profiles."""
    # Create multiple creator profiles
    users = UserFactory.create_batch(3)
    profiles = [user.creator_profile for user in users]

    url = reverse('creators:creator_profiles_list')

    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    for profile in profiles:
        assert profile.user.first_name in content
        assert profile.user.last_name in content
        assert "bio" in content


@pytest.mark.django_db
def test_creator_public_view(client, user_factory):
    """Test the public view of a creator profile."""
    creator_profile = user_factory.creator_profile

    url = reverse('creators:creator_public_view', args=[creator_profile.user.slug])

    response = client.get(url)

    assert response.status_code == 200
    assert creator_profile.user.first_name in response.content.decode()
    assert creator_profile.user.last_name in response.content.decode()
    assert "bio" in response.content.decode()
    assert creator_profile.user.slug in response.content.decode()
    assert creator_profile.user.username in response.content.decode()
    assert creator_profile.website in response.content.decode()
    assert str(creator_profile.followers_count) in response.content.decode()
    assert str(creator_profile.rating) in response.content.decode()
    assert str(creator_profile.verified).lower() in response.content.decode()
    # asert images
    profile_image_url = creator_profile.profile_image.url if creator_profile.profile_image else ''
    cover_image_url = creator_profile.cover_image.url if creator_profile.cover_image else ''
    assert profile_image_url in response.content.decode()
    assert cover_image_url in response.content.decode()

@pytest.mark.django_db
def test_creator_public_view_not_found(client):
    """Test that a non-existent creator profile returns 404."""
    url = reverse('creators:creator_public_view', args=['non-existent-slug'])

    response = client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_creator_public_view_inactive_profile(client, user_factory):
    """Test that an inactive creator profile returns 404."""
    creator_profile = user_factory.creator_profile
    creator_profile.status = "inactive"
    creator_profile.save()

    url = reverse('creators:creator_public_view', args=[creator_profile.user.slug])

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_creator_public_view_content(client, user_factory):
    """Test that the creator public view displays correct content."""
    creator_profile = user_factory.creator_profile
    creator_profile.bio = "This is a test bio for the creator."
    creator_profile.website = "https://example.com"
    creator_profile.save()

    url = reverse('creators:creator_public_view', args=[creator_profile.user.slug])

    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "This is a test bio for the creator." in content
    assert "https://example.com" in content


@pytest.mark.django_db
def test_creator_public_view_multiple_profiles(client):
    """Test that multiple creator profiles can be accessed correctly."""
    users = UserFactory.create_batch(5)
    profiles = [user.creator_profile for user in users]

    for profile in profiles:
        url = reverse('creators:creator_public_view', args=[profile.user.slug])
        response = client.get(url)
        assert response.status_code == 200
        assert profile.user.first_name in response.content.decode()
        assert profile.user.last_name in response.content.decode()
        assert "bio" in response.content.decode()

    
@pytest.mark.django_db
def test_creator_public_view_slug_case_insensitivity(client, user_factory):
    """Test that the creator public view is case insensitive regarding slugs."""
    creator_profile = user_factory.creator_profile

    url = reverse('creators:creator_public_view', args=[creator_profile.user.slug.upper()])

    response = client.get(url)

    assert response.status_code == 200
    assert creator_profile.user.first_name in response.content.decode()
    assert creator_profile.user.last_name in response.content.decode()
    assert "bio" in response.content.decode()


@pytest.mark.django_db
def test_creator_public_view_special_characters_in_slug(client, user_factory):
    """Test that the creator public view handles special characters in slugs."""
    creator_profile = user_factory.creator_profile
    creator_profile.user.slug = "specialchar_slug-123"
    creator_profile.user.save()

    url = reverse('creators:creator_public_view', args=[creator_profile.user.slug])
    response = client.get(url)

    assert response.status_code == 200
    assert creator_profile.user.first_name in response.content.decode()
    assert creator_profile.user.last_name in response.content.decode()
    assert "bio" in response.content.decode()


@pytest.mark.django_db
def test_creator_public_view_redirects(client, user_factory):
    """Test that the creator public view redirects correctly if needed."""
    creator_profile = user_factory.creator_profile

    url = reverse('creators:creator_public_view', args=[creator_profile.user.slug]) + '?ref=homepage'

    response = client.get(url)

    assert response.status_code == 200
    assert creator_profile.user.first_name in response.content.decode()
    assert creator_profile.user.last_name in response.content.decode()
    assert "bio" in response.content.decode()