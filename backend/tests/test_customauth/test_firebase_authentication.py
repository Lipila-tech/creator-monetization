"""
Tests for Firebase authentication with user_type support.
"""
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from apps.creators.models import CreatorProfile
from rest_framework.test import APIRequestFactory
from utils.authentication import FirebaseAuthentication

User = get_user_model()


@pytest.mark.django_db
class TestFirebaseAuthenticationUserType:
    """Test Firebase authentication with user_type handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.auth = FirebaseAuthentication()
        self.factory = APIRequestFactory()

    def create_mock_request(self, token="test_token"):
        """Create a mock request with Bearer token."""
        request = self.factory.get("/")
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        return request

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_creates_user_with_creator_type_default(self, mock_verify):
        """Test that Firebase auth creates a user with user_type='creator' by default."""
        # Mock Firebase token verification
        mock_verify.return_value = {
            "name": "firebase_user_123",
            "email": "test@example.com",
        }

        request = self.create_mock_request()
        result = self.auth.authenticate(request)

        assert result is not None
        user, auth_data = result
        assert user.username == "firebase_user_123"
        assert user.email == "test@example.com"
        assert user.user_type == "creator"  # Should default to 'creator'
        assert auth_data is None

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_creates_creator_profile_automatically(self, mock_verify):
        """Test that creating a Firebase user with user_type='creator' triggers CreatorProfile creation."""
        mock_verify.return_value = {
            "name": "firebase_creator_123",
            "email": "creator@example.com",
            "role": "creator",
        }

        # Ensure no existing users
        initial_user_count = User.objects.count()

        request = self.create_mock_request()
        user, _ = self.auth.authenticate(request)

        # Verify user was created
        assert User.objects.count() == initial_user_count + 1

        # Verify CreatorProfile was automatically created by signal
        assert CreatorProfile.objects.filter(user=user).exists()
        creator_profile = CreatorProfile.objects.get(user=user)
        assert creator_profile.user == user
        assert creator_profile.status == "active"

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_respects_custom_user_type_claim(self, mock_verify):
        """Test that Firebase custom claims can override default user_type."""
        mock_verify.return_value = {
            "name": "firebase_admin_123",
            "email": "admin@example.com",
            "role": "admin",  # Custom claim
        }

        request = self.create_mock_request()
        user, _ = self.auth.authenticate(request)

        assert user.user_type == "admin"
        # Admin users should NOT have CreatorProfile
        assert not CreatorProfile.objects.filter(user=user).exists()

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_with_staff_user_type(self, mock_verify):
        """Test Firebase auth with staff user_type."""
        mock_verify.return_value = {
            "name": "firebase_staff_123",
            "email": "staff@example.com",
            "role": "staff",
        }

        request = self.create_mock_request()
        user, _ = self.auth.authenticate(request)

        assert user.user_type == "staff"
        assert not CreatorProfile.objects.filter(user=user).exists()

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_ignores_invalid_user_type_claim(self, mock_verify):
        """Test that invalid user_type claims are ignored and defaults to 'creator'."""
        mock_verify.return_value = {
            "name": "firebase_invalid_123",
            "email": "invalid@example.com",
            "role": "invalid_type",  # Invalid claim
        }

        request = self.create_mock_request()
        user, _ = self.auth.authenticate(request)

        # Should default to 'creator' when invalid
        assert user.user_type == "creator"
        assert CreatorProfile.objects.filter(user=user).exists()

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_existing_user_sync_email(self, mock_verify):
        """Test that subsequent logins sync email if changed."""
        # Create initial user
        initial_token = {
            "name": "firebase_sync_123",
            "email": "original@example.com",
        }
        mock_verify.return_value = initial_token
        request = self.create_mock_request()
        user_1, _ = self.auth.authenticate(request)

        assert user_1.email == "original@example.com"

        # Simulate second login with updated username
        updated_token = {
            "name": "firebase_updated_123",
            "email": "original@example.com",
        }
        mock_verify.return_value = updated_token
        request = self.create_mock_request()
        user_2, _ = self.auth.authenticate(request)

        # Should be same user with updated username
        assert user_2.id == user_1.id
        assert user_2.username == "firebase_updated_123"

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_existing_user_sync_user_type(self, mock_verify):
        """Test that user_type changes are synced on subsequent logins."""
        # Create initial creator user
        initial_token = {
            "name": "firebase_type_sync_123",
            "email": "typesync@example.com",
        }
        mock_verify.return_value = initial_token
        request = self.create_mock_request()
        user_1, _ = self.auth.authenticate(request)

        assert user_1.user_type == "creator"
        assert CreatorProfile.objects.filter(user=user_1).exists()

        # Simulate second login with different user_type
        updated_token = {
            "name": "firebase_type_sync_123",
            "email": "typesync@example.com",
            "role": "admin",
        }
        mock_verify.return_value = updated_token
        request = self.create_mock_request()
        user_2, _ = self.auth.authenticate(request)

        # Should be same user with updated user_type
        assert user_2.id == user_1.id
        assert user_2.user_type == "admin"
        # CreatorProfile should be deleted when user_type changes away from 'creator'
        assert not CreatorProfile.objects.filter(user=user_2).exists()

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_no_authorization_header(self, mock_verify):
        """Test that missing authorization header returns None."""
        request = self.factory.get("/")
        result = self.auth.authenticate(request)
        assert result is None
        mock_verify.assert_not_called()

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_invalid_authorization_header(self, mock_verify):
        """Test that non-Bearer authorization header returns None."""
        request = self.factory.get("/")
        request.META["HTTP_AUTHORIZATION"] = "Bearer"
        result = self.auth.authenticate(request)
        assert result is None
        mock_verify.assert_not_called()

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_empty_token(self, mock_verify):
        """Test that empty token raises AuthenticationFailed."""
        from rest_framework.exceptions import AuthenticationFailed

        request = self.factory.get("/")
        request.META["HTTP_AUTHORIZATION"] = "Bearer "
        
        with pytest.raises(AuthenticationFailed, match="Missing Firebase token"):
            self.auth.authenticate(request)

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_invalid_token(self, mock_verify):
        """Test that invalid Firebase token raises AuthenticationFailed."""
        from rest_framework.exceptions import AuthenticationFailed

        mock_verify.side_effect = Exception("Invalid token")
        request = self.create_mock_request("invalid_token")

        with pytest.raises(AuthenticationFailed, match="Invalid or expired Firebase token"):
            self.auth.authenticate(request)

    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_missing_email(self, mock_verify):
        """Test that missing email raises Authentication failed"""
        from rest_framework.exceptions import AuthenticationFailed
        
        mock_verify.return_value = {
                "name": "testuser",
                }
        request = self.create_mock_request()

        with pytest.raises(AuthenticationFailed, match="Invalid email"):
            self.auth.authenticate(request)


    @patch("utils.authentication.auth.verify_id_token")
    def test_firebase_auth_attaches_token_to_request(self, mock_verify):
        """Test that decoded token is attached to request."""
        mock_verify.return_value = {
            "username": "firebase_attach_123",
            "email": "attach@example.com",
        }

        request = self.create_mock_request()
        self.auth.authenticate(request)

        assert hasattr(request, "firebase_user")
        assert request.firebase_user["username"] == "firebase_attach_123"
        assert hasattr(request, "firebase_picture")
