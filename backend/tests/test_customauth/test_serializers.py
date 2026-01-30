"""
Tests for authentication serializers.
"""
import pytest
from django.contrib.auth import get_user_model
from apps.customauth.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
)
from tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializer:
    """Test UserSerializer."""

    def test_serialize_user(self):
        """Test serializing a user."""
        user = UserFactory(user_type="creator")
        serializer = UserSerializer(user)
        
        assert serializer.data['email'] == user.email
        assert serializer.data['username'] == user.username
        assert serializer.data['user_type'] == 'creator'
        assert 'password' not in serializer.data

    def test_user_serializer_fields(self):
        """Test all expected fields are present."""
        user = UserFactory()
        serializer = UserSerializer(user)
        expected_fields = {'id', 'email', 'username', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined', 'slug'}
        assert set(serializer.data.keys()) == expected_fields

    def test_user_type_is_read_only(self):
        """Test user_type field is read-only."""
        user = UserFactory(user_type="creator")
        data = {
            'user_type': 'admin',
            'first_name': 'Test'
        }
        serializer = UserSerializer(user, data=data, partial=True)
        assert serializer.is_valid()
        serializer.save()
        
        user.refresh_from_db()
        assert user.user_type == 'creator'  # Should not change


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    """Test UserRegistrationSerializer."""

    def test_register_valid_user(self):
        """Test registering a user with valid data."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.email == 'newuser@example.com'
        assert user.user_type == 'creator'
        assert user.check_password('SecurePass123!')

    def test_register_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors

    def test_register_weak_password(self):
        """Test registration fails with weak password."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': '123',
            'password2': '123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors

    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email."""
        UserFactory(email='existing@example.com')
        data = {
            'email': 'existing@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_register_duplicate_username(self):
        """Test registration fails with duplicate username."""
        UserFactory(username='existinguser')
        data = {
            'email': 'newuser@example.com',
            'username': 'existinguser',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_register_missing_required_fields(self):
        """Test registration fails when missing required fields."""
        data = {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_registered_user_is_creator(self):
        """Test newly registered user is always a creator."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        
        user = serializer.save()
        assert user.user_type == 'creator'
        assert user.is_staff is False


@pytest.mark.django_db
class TestCustomTokenObtainPairSerializer:
    """Test CustomTokenObtainPairSerializer."""

    def test_token_claims_include_user_data(self):
        """Test token includes custom user claims."""
        user = UserFactory(email='test@example.com', username='testuser', user_type='creator')
        
        serializer = CustomTokenObtainPairSerializer()
        token = serializer.get_token(user)
        
        assert token['email'] == 'test@example.com'
        assert token['username'] == 'testuser'
        assert token['user_type'] == 'creator'
        assert token['is_staff'] is False

    def test_token_claims_admin_user(self):
        """Test token includes is_staff for admin users."""
        user = UserFactory(user_type='admin', is_staff=True)
        
        serializer = CustomTokenObtainPairSerializer()
        token = serializer.get_token(user)
        
        assert token['is_staff'] is True
        assert token['user_type'] == 'admin'

    def test_token_full_name(self):
        """Test token includes full name."""
        user = UserFactory(first_name='John', last_name='Doe')
        
        serializer = CustomTokenObtainPairSerializer()
        token = serializer.get_token(user)
        
        assert token['full_name'] == 'John Doe'


@pytest.mark.django_db
class TestChangePasswordSerializer:
    """Test ChangePasswordSerializer."""

    def test_change_password_valid(self, rf):
        """Test changing password with valid data."""
        user = UserFactory(password='OldPass123!')
        request = rf.post('/')
        request.user = user
        
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        serializer = ChangePasswordSerializer(
            user,
            data=data,
            context={'request': request}
        )
        assert serializer.is_valid()
        
        serializer.save()
        user.refresh_from_db()
        assert user.check_password('NewPass456!')

    def test_change_password_incorrect_old_password(self, rf):
        """Test change password fails with incorrect old password."""
        user = UserFactory(password='OldPass123!')
        request = rf.post('/')
        request.user = user
        
        data = {
            'old_password': 'WrongPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        serializer = ChangePasswordSerializer(
            user,
            data=data,
            context={'request': request}
        )
        assert not serializer.is_valid()
        assert 'old_password' in serializer.errors

    def test_change_password_mismatch(self, rf):
        """Test change password fails when new passwords don't match."""
        user = UserFactory(password='OldPass123!')
        request = rf.post('/')
        request.user = user
        
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'DifferentPass123!'
        }
        serializer = ChangePasswordSerializer(
            user,
            data=data,
            context={'request': request}
        )
        assert not serializer.is_valid()
        assert 'new_password' in serializer.errors

    def test_change_password_weak_new_password(self, rf):
        """Test change password fails with weak new password."""
        user = UserFactory(password='OldPass123!')
        request = rf.post('/')
        request.user = user
        
        data = {
            'old_password': 'OldPass123!',
            'new_password': '123',
            'new_password2': '123'
        }
        serializer = ChangePasswordSerializer(
            user,
            data=data,
            context={'request': request}
        )
        assert not serializer.is_valid()
        assert 'new_password' in serializer.errors
