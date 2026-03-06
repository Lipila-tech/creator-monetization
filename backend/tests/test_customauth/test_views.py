"""
Tests for authentication views.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from tests.factories import UserFactory, StaffUserFactory

User = get_user_model()

@pytest.mark.django_db
class TestLoginRateLimiting:
    """Test login rate limiting."""

    def test_login_rate_limit_exceeded(self, auth_api_client):
        """Test login fails after exceeding rate limit."""
        email = 'test@example.com'
        UserFactory(email=email, password='TestPass123!')

        # Attempt login multiple times to exceed rate limit
        login_url = reverse('customauth:login')
        for _ in range(6):  # Exceed the rate limit
            login_data = {'email': email, 'password': 'WrongPass123!'}
            auth_api_client.post(login_url, login_data, format='json')

        # Verify login fails after exceeding rate limit
        login_data = {'email': email, 'password': 'TestPass123!'}
        response = auth_api_client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_login_rate_limit_resets_after_timeout(self, auth_api_client):
        """Test login rate limit resets after timeout."""
        email = 'test@example.com'
        UserFactory(email=email, password='TestPass123!')

        # Attempt login multiple times to exceed rate limit
        login_url = reverse('customauth:login')
        for _ in range(6):  # Exceed the rate limit
            login_data = {'email': email, 'password': 'WrongPass123!'}
            auth_api_client.post(login_url, login_data, format='json')

        # Verify login fails after exceeding rate limit
        login_data = {'email': email, 'password': 'TestPass123!'}
        response = auth_api_client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        # Simulate waiting for timeout (30 minutes)
        from django.core.cache import cache
        cache.clear()  # Clear cache to reset rate limit
        # Verify login succeeds after timeout        
        response = auth_api_client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_login_rate_limit_different_users(self, auth_api_client):
        """Test login rate limit is per user."""
        email1 = 'user1@example.com'
        email2 = 'user2@example.com'
        UserFactory(email=email1, password='TestPass123!')
        UserFactory(email=email2, password='TestPass123!')

        # Attempt login for both users to exceed rate limit
        login_url = reverse('customauth:login')
        for _ in range(6):  # Exceed the rate limit
            login_data = {'email': email1, 'password': 'WrongPass123!'}
            auth_api_client.post(login_url, login_data, format='json')

        # Verify login fails for user1 after exceeding rate limit
        login_data = {'email': email1, 'password': 'TestPass123!'}
        response = auth_api_client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

        # Verify login failes for user2 same IP used but different email
        login_data = {'email': email2, 'password': 'TestPass123!'}
        response = auth_api_client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


    def test_login_after_third_attempt_succeeds(self, auth_api_client):
        """Test login success fails after 3 failed attempts. before hitting the rate limit. """
        email = 'test@example.com'
        UserFactory(email=email, password='TestPass123!')
        login_url = reverse('customauth:login')
        for _ in range(2):  # 2 failed attempts
            login_data = {'email': email, 'password': 'WrongPass123!'}
            auth_api_client.post(login_url, login_data, format='json')
        # Verify login still succeeds on 4th attempt (before hitting rate limit)
        login_data = {'email': email, 'password': 'TestPass123!'}
        response = auth_api_client.post(login_url, login_data, format='json')
        assert response.status_code == status.HTTP_200_OK
       

@pytest.mark.django_db
class TestUserRegistrationView:
    """Test user registration endpoint."""

    def test_register_creator_success(self, auth_api_client):
        """Test successful creator registration."""
        data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['email'] == 'newcreator@example.com'
        assert response.data['user']['user_type'] == 'creator'
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_register_invalid_password_length(self, auth_api_client):
        """Test registration fails with invalid password length."""
        data = {
            'email': 'newcreator@example.com',
            'username': 'newcreator',
            'password': '123',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_register_duplicate_email(self, auth_api_client):
        """Test registration fails with duplicate email."""
        UserFactory(email='existing@example.com')
        data = {
            'email': 'existing@example.com',
            'username': 'newcreator',
            'password': 'SecurePass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_username(self, auth_api_client):
        """Test registration fails with duplicate username."""
        UserFactory(username='existinguser')
        data = {
            'email': 'newcreator@example.com',
            'username': 'existinguser',
            'password': 'SecurePass123!',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        url = reverse('customauth:user_register')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCustomLoginView:
    """Test email/password login endpoint."""

    def test_login_success(self, auth_api_client):
        """Test successful login."""
        UserFactory(email='test@example.com', password='TestPass123!')
        url = reverse('customauth:login')

        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_login_invalid_email(self, auth_api_client):
        """Test login fails with invalid email."""
        url = reverse('customauth:login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password'
        }
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_invalid_password(self, auth_api_client):
        """Test login fails with invalid password."""
        UserFactory(email='test@example.com', password='TestPass123!')
        url = reverse('customauth:login')
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_token_contains_custom_claims(self, auth_api_client):
        """Test token contains custom claims."""
        UserFactory(
            email='test@example.com',
            password='TestPass123!',
            user_type='creator'
        )
        url = reverse('customauth:login')

        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        # Token contains custom claims (verify by decoding)
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken(response.data['access_token'])
        assert token['email'] == 'test@example.com'
        assert token['user_type'] == 'creator'

    def test_login_staff_user(self, auth_api_client):
        """Test staff user can login."""
        StaffUserFactory(email='staff@example.com', password='TestPass123!')
        url = reverse('customauth:login')

        data = {
            'email': 'staff@example.com',
            'password': 'TestPass123!'
        }
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestTokenRefreshView:
    """Test token refresh endpoint."""

    def test_refresh_token_success(self, auth_api_client):
        """Test successful token refresh."""
        user = UserFactory()
        refresh = RefreshToken.for_user(user)
        url = reverse('customauth:token_refresh')
        data = {'refresh': str(refresh)}

        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data

    def test_refresh_invalid_token(self, auth_api_client):
        """Test refresh fails with invalid token."""
        url = reverse('customauth:token_refresh')
        data = {'refresh': 'invalid_token'}
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_missing(self, auth_api_client):
        """Test refresh fails when token is missing."""
        url = reverse('customauth:token_refresh')
        data = {}
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfileView:
    """Test user profile endpoint."""

    def test_get_profile_authenticated(self, auth_api_client):
        """Test getting profile when authenticated."""
        user = UserFactory(first_name='John', last_name='Doe')
        auth_api_client.force_authenticate(user=user)

        url = reverse('customauth:user_profile')
        response = auth_api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['email'] == user.email
        assert response.data['data']['first_name'] == 'John'

    def test_get_profile_not_authenticated(self, auth_api_client):
        """Test getting profile without authentication."""
        url = reverse('customauth:user_profile')
        response = auth_api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_patch(self, auth_api_client):
        """Test updating profile with PATCH."""
        user = UserFactory(first_name='John', last_name='Doe')
        auth_api_client.force_authenticate(user=user)

        data = {'firstName': 'Jane'}
        url = reverse('customauth:user_profile')
        response = auth_api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['first_name'] == 'Jane'
        assert response.data['data']['last_name'] == 'Doe'

        user.refresh_from_db()
        assert user.first_name == 'Jane'

    def test_update_profile_put(self, auth_api_client):
        """Test updating profile with PUT."""
        user = UserFactory(first_name='John', last_name='Doe')
        auth_api_client.force_authenticate(user=user)

        data = {
            'firstName': 'Jane',
            'lastName': 'Smith',
            'email': user.email,
            'username': user.username
        }
        url = reverse('customauth:user_profile')
        response = auth_api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['first_name'] == 'Jane'
        assert response.data['data']['last_name'] == 'Smith'

    def test_cannot_change_user_type_via_api(self, auth_api_client):
        """Test user_type cannot be changed via profile update endpoint."""
        user = UserFactory(user_type='creator')
        auth_api_client.force_authenticate(user=user)

        data = {'user_type': 'admin', 'first_name': 'Test'}
        url = reverse('customauth:user_profile')
        auth_api_client.patch(url, data, format='json')

        user.refresh_from_db()
        assert user.user_type == 'creator'

    def test_update_profile_invalid_data(self, auth_api_client):
        """Test profile update with invalid data."""
        user = UserFactory()
        auth_api_client.force_authenticate(user=user)

        data = {'email': 'invalid_email'}
        url = reverse('customauth:user_profile')
        response = auth_api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestChangePasswordView:
    """Test change password endpoint."""

    def test_change_password_success(self, auth_api_client):
        """Test successful password change."""
        user = UserFactory(password='OldPass123!')
        auth_api_client.force_authenticate(user=user)

        data = {
            'oldPassword': 'OldPass123!',
            'newPassword': 'NewPass456!',
        }
        url = reverse('customauth:change_password')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.check_password('NewPass456!')

    def test_change_password_not_authenticated(self, auth_api_client):
        """Test change password requires authentication."""
        data = {
            'oldPassword': 'OldPass123!',
            'newPassword': 'NewPass456!',
        }
        url = reverse('customauth:change_password')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_incorrect_old(self, auth_api_client):
        """Test change password fails with incorrect old password."""
        user = UserFactory(password='OldPass123!')
        auth_api_client.force_authenticate(user=user)

        data = {
            'oldPassword': 'WrongPass123!',
            'newPassword': 'NewPass456!',
        }
        url = reverse('customauth:change_password')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    
    def test_change_password_weak_new_password(self, auth_api_client):
        """Test change password fails with weak new password."""
        user = UserFactory(password='OldPass123!')
        auth_api_client.force_authenticate(user=user)

        data = {
            'oldPassword': 'OldPass123!',
            'newPassword': '123'
        }
        url = reverse('customauth:change_password')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutView:
    """Test logout endpoint."""

    def test_logout_success(self, auth_api_client):
        """Test successful logout."""
        user = UserFactory()
        auth_api_client.force_authenticate(user=user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        data = {'refresh': str(refresh)}
        url = reverse('customauth:logout')
        response = auth_api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

    def test_logout_not_authenticated(self, auth_api_client):
        """Test logout requires authentication."""
        url = reverse('customauth:logout')
        response = auth_api_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_without_refresh_token(self, auth_api_client):
        """Test logout without refresh token still succeeds."""
        user = UserFactory()
        auth_api_client.force_authenticate(user=user)

        url = reverse('customauth:logout')
        response = auth_api_client.post(url, {}, format='json')

        # Should still succeed (gracefully handle missing token)
        assert response.status_code == status.HTTP_200_OK

    def test_logout_invalid_refresh_token(self, auth_api_client):
        """Test logout with invalid refresh token."""
        user = UserFactory()
        auth_api_client.force_authenticate(user=user)

        data = {'refresh': 'invalid_token'}
        url = reverse('customauth:logout')
        response = auth_api_client.post(url, data, format='json')

        # Should handle gracefully
        assert response.status_code in [
            status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
