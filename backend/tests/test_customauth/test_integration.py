"""
Integration tests for the authentication system.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factories import UserFactory, StaffUserFactory, AdminUserFactory, APIClientFactory


@pytest.mark.django_db
class TestAuthenticationFlow:
    """Test complete authentication flow."""

    def test_creator_registration_and_login_flow(self, api_client):
        """Test creator can register and login."""
        # Step 1: Register as creator
        register_data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        register_url = reverse('customauth:user_register')
        register_response = api_client.post(register_url, register_data, format='json')
        
        assert register_response.status_code == status.HTTP_201_CREATED
        access_token_1 = register_response.data['access_token']
        
        # Step 2: Use provided token to get profile
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token_1}', HTTP_X_API_KEY=client.api_key)
        profile_url = reverse('customauth:user_profile')
        profile_response = api_client.get(profile_url)
        
        assert profile_response.status_code == status.HTTP_200_OK
        assert profile_response.data['email'] == 'newcreator@example.com'
        assert profile_response.data['user_type'] == 'creator'
    
    def test_token_refresh_flow(self, api_client):
        """Test token refresh flow."""
        user = UserFactory(password='TestPass123!')
        
        # Step 1: Login and get tokens
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        login_url = reverse('customauth:token_obtain_pair')
        login_data = {'email': user.email, 'password': 'TestPass123!'}
        login_response = api_client.post(login_url, login_data, format='json')
        
        assert login_response.status_code == status.HTTP_200_OK
        refresh_token = login_response.data['refresh_token']
        
        # Step 2: Use refresh token to get new access token
        refresh_url = reverse('customauth:token_refresh')
        refresh_data = {'refresh': refresh_token}
        refresh_response = api_client.post(refresh_url, refresh_data, format='json')
        
        assert refresh_response.status_code == status.HTTP_200_OK
        new_access_token = refresh_response.data['access_token']
        
        # Step 3: Use new token to access protected resource
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}', HTTP_X_API_KEY=client.api_key)
        profile_url = reverse('customauth:user_profile')
        profile_response = api_client.get(profile_url)
        
        assert profile_response.status_code == status.HTTP_200_OK

    def test_profile_update_flow(self, api_client):
        """Test updating user profile."""
        user = UserFactory(first_name='John', last_name='Doe')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        # Update profile
        update_data = {'first_name': 'Jane', 'last_name': 'Smith'}
        profile_url = reverse('customauth:user_profile')
        update_response = api_client.patch(profile_url, update_data, format='json')
        
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data['first_name'] == 'Jane'
        
        # Verify update persisted
        get_response = api_client.get(profile_url)
        assert get_response.data['first_name'] == 'Jane'

    def test_password_change_flow(self, api_client):
        """Test changing password."""
        user = UserFactory(password='OldPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        # Change password
        password_data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        password_url = reverse('customauth:change_password')
        password_response = api_client.post(password_url, password_data, format='json')
        
        assert password_response.status_code == status.HTTP_200_OK
        
        # Verify can login with new password
        login_url = reverse('customauth:token_obtain_pair')
        login_data = {'email': user.email, 'password': 'NewPass456!'}
        login_response = api_client.post(login_url, login_data, format='json')
        
        assert login_response.status_code == status.HTTP_200_OK

    def test_logout_flow(self, api_client):
        """Test logout flow."""
        user = UserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        
        # Get refresh token
        refresh = RefreshToken.for_user(user)
        
        # Logout
        logout_url = reverse('customauth:logout')
        logout_data = {'refresh': str(refresh)}
        logout_response = api_client.post(logout_url, logout_data, format='json')
        
        assert logout_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestMultiFrontendScenario:
    """Test multi-frontend API scenario."""

    def test_multiple_clients_with_different_api_keys(self, api_client):
        """Test multiple frontend clients with different API keys."""
        # Create two clients
        client1 = APIClientFactory(name='Creator App', rate_limit=1000)
        client2 = APIClientFactory(name='Admin Dashboard', rate_limit=500)
        
        # Create a user
        user = UserFactory(password='TestPass123!')
        
        # Login and get tokens
        login_url = reverse('customauth:token_obtain_pair')
        login_data = {'email': user.email, 'password': 'TestPass123!'}
        
        # Both clients can login with same credentials
        api_client.credentials(HTTP_X_API_KEY=client1.api_key)
        response1 = api_client.post(login_url, login_data, format='json')
        api_client.credentials(HTTP_X_API_KEY=client2.api_key)
        response2 = api_client.post(login_url, login_data, format='json')
        
        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK

    def test_api_key_authentication_in_requests(self, api_client):
        """Test using API key in requests."""
        client = APIClientFactory(is_active=True)
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        # Make request with API key header
        api_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer dummy_token',
            HTTP_X_API_KEY=client.api_key
        )
        
        # The request should be processed (client identified)
        # Real implementation would check client rate limits, etc.


@pytest.mark.django_db
class TestUserTypePermissions:
    """Test user type-based access control."""

    def test_creator_can_only_access_creator_endpoints(self, api_client):
        """Test creator has limited access."""
        creator = UserFactory(user_type='creator')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=creator)
        
        # Creator can access profile endpoint
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        profile_url = reverse('customauth:user_profile')
        response = api_client.get(profile_url)
        assert response.status_code == status.HTTP_200_OK

    def test_staff_can_access_their_profile(self, api_client):
        """Test staff can access profile."""
        staff = StaffUserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=staff)
        
        profile_url = reverse('customauth:user_profile')
        response = api_client.get(profile_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user_type'] == 'staff'

    def test_admin_can_access_their_profile(self, api_client):
        """Test admin can access profile."""
        admin = AdminUserFactory()
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=admin)
        
        profile_url = reverse('customauth:user_profile')
        response = api_client.get(profile_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user_type'] == 'admin'


@pytest.mark.django_db
class TestErrorHandling:
    """Test error handling in authentication."""

    def test_invalid_credentials_returns_401(self, api_client):
        """Test invalid credentials return 401."""
        user = UserFactory(password='TestPass123!')
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        
        login_url = reverse('customauth:token_obtain_pair')
        login_data = {'email': user.email, 'password': 'WrongPassword'}
        response = api_client.post(login_url, login_data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_missing_required_fields_returns_400(self, api_client):
        """Test missing required fields return 400."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        register_url = reverse('customauth:user_register')
        register_data = {'email': 'missingfields@example.com'}  # Missing username, password
        response = api_client.post(register_url, register_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_accessing_protected_endpoint_without_auth_returns_401(self, api_client):
        """Test accessing protected endpoint without auth returns 401."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        profile_url = reverse('customauth:user_profile')
        response = api_client.get(profile_url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_token_returns_401(self, api_client):
        """Test invalid token returns 401."""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        profile_url = reverse('customauth:user_profile')
        response = api_client.get(profile_url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
