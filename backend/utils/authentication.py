from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from apps.customauth.models import APIClient
from rest_framework import authentication, exceptions
from firebase_admin import auth

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
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
        name = decoded_token.get("name", "")
        picture = decoded_token.get("picture", "")

        if not firebase_uid:
            raise exceptions.AuthenticationFailed("Firebase UID not found.")

        user, _ = User.objects.get_or_create(
            username=firebase_uid,
            defaults={
                "email": email or "",
                "first_name": name or "",
            },
        )

        # optional sync
        if email and user.email != email:
            user.email = email
            user.save(update_fields=["email"])

        # attach decoded token if you want later access
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
