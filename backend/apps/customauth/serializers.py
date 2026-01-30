from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """Custom serializer for refreshing JWT tokens."""

    def validate(self, attrs):
        """Validate and return new access token."""
        data = super().validate(attrs)
        return data

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined', 'slug')
        read_only_fields = ('id', 'user_type', 'date_joined', 'is_active', 'slug')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return attrs

    def create(self, validated_data):
        """Create user as creator with hashed password."""
        # Creators self-register, so force user_type to 'creator'
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type='creator'  # Self-registered users are creators
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user data."""

    @classmethod
    def get_token(cls, user):
        """Override to add custom claims."""
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['user_type'] = user.user_type
        token['full_name'] = user.get_full_name()
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        """Override to use email instead of username."""
        data = super().validate(attrs)
        return data


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer for token refresh."""

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(
        write_only=True,
        required=True
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['new_password'] != attrs.pop('new_password2'):
            raise serializers.ValidationError({
                'new_password': 'Passwords do not match.'
            })
        return attrs

    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def update(self, instance, validated_data):
        """Update user password."""
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
