from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from utils.authentication import RequireAPIKey
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    CustomTokenRefreshSerializer
)

User = get_user_model()


class CustomTokenRefreshView(TokenRefreshView):
    """Custom JWT token refresh view."""
    permission_classes = [RequireAPIKey]
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to refresh JWT tokens.
        return json {access_token, refresh_token}
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            return Response({
                'access_token': data['access'],
                'refresh_token': data['refresh'],
            })
        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view."""
    permission_classes = [RequireAPIKey]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Login with email and password.

            Authenticates a user and returns access/refresh tokens to be used for
            subsequent requests.

            Authentication
            --------------
            Public endpoint.
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            return Response({
                'access_token': data['access'],
                'refresh_token': data['refresh'],
            })
        return response


class TokenRefreshView(TokenRefreshView):
    """JWT token refresh view."""
    permission_classes = [RequireAPIKey]
    serializer_class = TokenRefreshView.serializer_class

    def post(self, request, *args, **kwargs):
        """
        Refresh an access token.

        Exchanges a valid refresh token for a new access token.

        Authentication
        --------------
        Public endpoint (token-based).
        """
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            return Response({
                'access_token': data['access'],
            })
        return response


class UserRegistrationView(APIView):
    permission_classes = [RequireAPIKey]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """ Register a new user account (creator or patron).

        Creates a new account using email/password. The backend may assign roles
        (creator vs patron) during onboarding or via a separate profile endpoint.

        Authentication
        --------------
        Public endpoint."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Get current user profile."""
    serializer_class = UserSerializer
    permission_classes = [RequireAPIKey, IsAuthenticated]

    def get(self, request):
        """Get user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Update user profile."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Partially update user profile."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Change user password."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [RequireAPIKey, IsAuthenticated]

    def post(self, request):
        """Change password."""
        serializer = ChangePasswordSerializer(
            request.user,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    serializer_class = None
    permission_classes = [RequireAPIKey, IsAuthenticated]

    def post(self, request):
        """
            Logout / revoke refresh token (optional, recommended).

            Invalidates the refresh token server-side (if supported). Access tokens
            typically expire naturally.

            Authentication
            --------------
            Requires authentication.
            """
            
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'message': 'Successfully logged out.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

