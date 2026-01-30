import pytest
from tests.factories import UserFactory

@pytest.mark.django_db
def test_creating_a_user_with_creator_role_creates_creator_profile(client):
    """Test that creating a user with user_type 'creator' also creates a CreatorProfile."""
    user = UserFactory(user_type='creator')

    assert user.user_type == 'creator'
    assert hasattr(user, 'creator_profile')
    assert user.creator_profile.user == user
    assert user.creator_profile.status == 'active'