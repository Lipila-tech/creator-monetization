from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.conf import settings
from apps.customauth.models import APIClient
from rest_framework import authentication, exceptions
from firebase_admin import auth

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Firebase token-based authentication with user_type support.
    
    Creates or updates users with appropriate user_type based on Firebase custom claims
    or defaults to 'creator'. When a user with user_type='creator' is created, the
    post_save signal automatically triggers CreatorProfile creation.
    """
    
    def _get_user_type_from_token(self, decoded_token):
        """
        Extract user_type from Firebase custom claims.
        
        Args:
            decoded_token: The decoded Firebase ID token
            
        Returns:
            str: The user_type ('creator', 'admin', 'staff') from claims
                or 'creator' as default if not specified
        """
        # Check Firebase custom claims for user_type
        user_type = decoded_token.get("user_type")
        
        if user_type and user_type in dict(User.USER_TYPE_CHOICES):
            return user_type
        
        # Fall back to settings or default to 'creator'
        return getattr(settings, 'DEFAULT_USER_TYPE', 'creator')
    
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None

        id_token = auth_header.split("Bearer ")[1].strip()
        if not id_token:
            raise exceptions.AuthenticationFailed("Missing Firebase token.")

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid or expired Firebase token.")

        firebase_uid = decoded_token.get("uid")
        email = decoded_token.get("email", "")
        username = (decoded_token.get("name") or email.split("@")[0])
        user_type = decoded_token.get("role", "")
        picture = decoded_token.get("picture", "")
        
        if not isinstance(username, str) or not username.strip():
            raise exceptions.AuthenticationFailed("Invalid username")

        if not isinstance(email, str) or not email.strip():
            raise exceptions.AuthenticationFailed("Invalid email")
        
        allowed_roles = ["admin", "creator", "patron", "guest", "staff"]

        if user_type not in allowed_roles:
            user_type = "creator"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "user_type": user_type,  # Set user_type on creation (triggers CreatorProfile signal)
            },
        )

        # Sync email if changed
        if username and user.username != username:
            user.username = username
            user.save(update_fields=["username"])
        
        # Sync user_type if changed (this will trigger CreatorProfile creation/deletion signals)
        if user.user_type != user_type:
            user.user_type = user_type
            user.save(update_fields=["user_type"])

        # Attach decoded token if you want later access
        request.firebase_user = decoded_token
        request.firebase_picture = picture

        return (user, None)


class APIKeyAuthentication(BaseAuthentication):
    """
    Authentication using API keys for frontend clients.
    Useful for service-to-service communication and frontend identification.
    """

    def authenticate(self, request):
        """
        Authenticate using API key from request header.
        Format: X-API-Key: sk_xxxxx
        """
        api_key = request.META.get('HTTP_X_API_KEY')

        if not api_key:
            return None

        try:
            client = APIClient.objects.get(api_key=api_key, is_active=True)
        except APIClient.DoesNotExist:
            raise AuthenticationFailed('Invalid or inactive API key.')

        # Store client info in request for later use
        request.client = client
        # Return None to continue with JWT authentication
        return None

    def authenticate_header(self, request):
        """Return the authentication header."""
        return 'X-API-Key'


class RequireAPIKey(BasePermission):
    """
    Permission class to require API key authentication for frontend clients.
    """
    message = 'API key is required. Please provide X-API-Key header.'

    def has_permission(self, request, view):
        """Check if request has valid API key."""
        return hasattr(request, 'client') and request.client is not None


class ClientIdentificationMiddleware:
    """
    Middleware to identify the client making the request.
    Useful for multi-frontend API with client-specific behavior.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to identify client from API key
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                client = APIClient.objects.get(api_key=api_key, is_active=True)
                request.client = client
            except APIClient.DoesNotExist:
                pass

        # Try to identify from X-Client-ID header
        client_id = request.META.get('HTTP_X_CLIENT_ID')
        if client_id and not hasattr(request, 'client'):
            try:
                client = APIClient.objects.get(id=client_id, is_active=True)
                request.client = client
            except APIClient.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
