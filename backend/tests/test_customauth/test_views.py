"""
Tests for authentication views.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from tests.factories import UserFactory, StaffUserFactory, APIClientFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistrationView:
    """Test user registration endpoint."""

    def test_register_creator_success(self, api_client):
        """Test successful creator registration."""
        data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        url = reverse('customauth:user_register')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['email'] == 'newcreator@example.com'
        assert response.data['user']['user_type'] == 'creator'
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_register_no_auth_required(self, api_client):
        """Test registration doesn't require authentication."""
        api_client.force_authenticate(user=None)
        data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        url = reverse('customauth:user_register')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_invalid_password(self, api_client):
        """Test registration fails with invalid password."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': '123',
            'password2': '123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_register_password_mismatch(self, api_client):
        """Test registration fails when passwords don't match."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_register_duplicate_email(self, api_client):
        """Test registration fails with duplicate email."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        UserFactory(email='existing@example.com')
        data = {
            'email': 'existing@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_username(self, api_client):
        """Test registration fails with duplicate username."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        UserFactory(username='existinguser')
        data = {
            'email': 'newcreator@example.com',
            'username': 'existinguser',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTokenObtainView:
    """Test JWT token obtain endpoint."""

    def test_login_success(self, api_client):
        """Test successful login."""
        UserFactory(email='test@example.com', password='TestPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        url = reverse('customauth:token_obtain_pair')
        
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_login_invalid_email(self, api_client):
        """Test login fails with invalid email."""
        url = reverse('customauth:token_obtain_pair')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_invalid_password(self, api_client):
        """Test login fails with invalid password."""
        UserFactory(email='test@example.com', password='TestPass123!')
        url = reverse('customauth:token_obtain_pair')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_token_contains_custom_claims(self, api_client):
        """Test token contains custom claims."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        UserFactory(
            email='test@example.com',
            password='TestPass123!',
            user_type='creator'
        )
        url = reverse('customauth:token_obtain_pair')
        
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        # Token contains custom claims (verify by decoding)
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken(response.data['access_token'])
        assert token['email'] == 'test@example.com'
        assert token['user_type'] == 'creator'

    def test_login_staff_user(self, api_client):
        """Test staff user can login."""
        StaffUserFactory(email='staff@example.com', password='TestPass123!')
        url = reverse('customauth:token_obtain_pair')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        
        data = {
            'email': 'staff@example.com',
            'password': 'TestPass123!'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestTokenRefreshView:
    """Test token refresh endpoint."""
  
    def test_refresh_token_success(self, api_client):
        """Test successful token refresh."""
        user = UserFactory()
        refresh = RefreshToken.for_user(user)
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        url = reverse('customauth:token_refresh')
        data = {'refresh': str(refresh)}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data

    def test_refresh_invalid_token(self, api_client):
        """Test refresh fails with invalid token."""
        url = reverse('customauth:token_refresh')
        data = {'refresh': 'invalid_token'}
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_missing(self, api_client):
        """Test refresh fails when token is missing."""
        url = reverse('customauth:token_refresh')
        data = {}
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfileView:
    """Test user profile endpoint."""

    def test_get_profile_authenticated(self, api_client):
        """Test getting profile when authenticated."""
        user = UserFactory(first_name='John', last_name='Doe')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        url = reverse('customauth:user_profile')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == 'John'

    def test_get_profile_not_authenticated(self, api_client):
        """Test getting profile without authentication."""
        url = reverse('customauth:user_profile')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_patch(self, api_client):
        """Test updating profile with PATCH."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        user = UserFactory(first_name='John', last_name='Doe')
        api_client.force_authenticate(user=user)
        
        data = {'first_name': 'Jane'}
        url = reverse('customauth:user_profile')
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Jane'
        assert response.data['last_name'] == 'Doe'
        
        user.refresh_from_db()
        assert user.first_name == 'Jane'

    def test_update_profile_put(self, api_client):
        """Test updating profile with PUT."""
        user = UserFactory(first_name='John', last_name='Doe')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': user.email,
            'username': user.username
        }
        url = reverse('customauth:user_profile')
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Jane'
        assert response.data['last_name'] == 'Smith'

    def test_cannot_change_user_type_via_api(self, api_client):
        """Test user_type cannot be changed via API."""
        user = UserFactory(user_type='creator')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {'user_type': 'admin', 'first_name': 'Test'}
        url = reverse('customauth:user_profile')
        response = api_client.patch(url, data, format='json')
        
        user.refresh_from_db()
        assert user.user_type == 'creator'

    def test_update_profile_invalid_data(self, api_client):
        """Test profile update with invalid data."""
        user = UserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {'email': 'invalid_email'}
        url = reverse('customauth:user_profile')
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestChangePasswordView:
    """Test change password endpoint."""

    def test_change_password_success(self, api_client):
        """Test successful password change."""
        user = UserFactory(password='OldPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        url = reverse('customauth:change_password')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        user.refresh_from_db()
        assert user.check_password('NewPass456!')

    def test_change_password_not_authenticated(self, api_client):
        """Test change password requires authentication."""
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        url = reverse('customauth:change_password')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_incorrect_old(self, api_client):
        """Test change password fails with incorrect old password."""
        user = UserFactory(password='OldPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'WrongPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        url = reverse('customauth:change_password')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_mismatch(self, api_client):
        """Test change password fails when new passwords don't match."""
        user = UserFactory(password='OldPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'DifferentPass123!'
        }
        url = reverse('customauth:change_password')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_weak_new_password(self, api_client):
        """Test change password fails with weak new password."""
        user = UserFactory(password='OldPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {
            'old_password': 'OldPass123!',
            'new_password': '123',
            'new_password2': '123'
        }
        url = reverse('customauth:change_password')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutView:
    """Test logout endpoint."""

    def test_logout_success(self, api_client):
        """Test successful logout."""
        user = UserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        data = {'refresh': str(refresh)}
        url = reverse('customauth:logout')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

    def test_logout_not_authenticated(self, api_client):
        """Test logout requires authentication."""
        url = reverse('customauth:logout')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.post(url, {}, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_without_refresh_token(self, api_client):
        """Test logout without refresh token still succeeds."""
        user = UserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        url = reverse('customauth:logout')
        response = api_client.post(url, {}, format='json')
        
        # Should still succeed (gracefully handle missing token)
        assert response.status_code == status.HTTP_200_OK

    def test_logout_invalid_refresh_token(self, api_client):
        """Test logout with invalid refresh token."""
        user = UserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        data = {'refresh': 'invalid_token'}
        url = reverse('customauth:logout')
        response = api_client.post(url, data, format='json')
        
        # Should handle gracefully
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
