from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    CustomUserSerializer,
    CustomUserRegistrationSerializer,
    CustomLoginSerializer,
    ChangePasswordSerializer,
    CustomTokenRefreshSerializer
)
from drf_spectacular.utils import extend_schema
from utils import serializers as helpers
from utils.authentication import RequireAPIKey

User = get_user_model()


class CustomTokenRefreshView(TokenRefreshView):
    """Custom JWT token refresh view."""
    permission_classes = [RequireAPIKey]
    serializer_class = CustomTokenRefreshSerializer
    
    @extend_schema(
        operation_id="token_refresh",
        summary="JWT Token Refresh",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
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


class CustomLoginView(TokenObtainPairView):
    """Custom Login view Using Email and Password"""
    permission_classes = [RequireAPIKey]
    serializer_class = CustomLoginSerializer
    throttle_scope = 'login_attempts'

    @extend_schema(
        operation_id="email_password_login",
        summary="Email & Password Login",
        request=CustomLoginSerializer,
        responses={
            200: helpers.LoginResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
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

class UserRegistrationView(APIView):
    permission_classes = [RequireAPIKey]
    serializer_class = CustomUserRegistrationSerializer

    @extend_schema(
        operation_id="email_password_register",
        summary="Email & Password Registration",
        request=CustomUserRegistrationSerializer,
        responses={
            201: helpers.RegistrationResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def post(self, request):
        """
        Register a new user account (creator or patron).

            Creates a new account using email/password. The backend auto assigns
            user_type (creator) if not provided. Frontend may request user_type change
            during onboarding via the Select User Type endpoint in Creators folder.

            Authentication
            --------------
            Public endpoint.
        """
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': CustomUserSerializer(user).data,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Get current user profile."""
    serializer_class = CustomUserSerializer
    permission_classes = [RequireAPIKey, IsAuthenticated]

    @extend_schema(
        operation_id="retrieve_profile",
        summary="Retrieve User Profile",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def get(self, request):
        """Get user profile."""
        serializer = CustomUserSerializer(request.user)
        return Response({
            'status': 'success',
            'data':serializer.data
        })

    @extend_schema(
        operation_id="update_profile",
        summary="Update User Profile",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def put(self, request):
        """Fully Update user profile."""
        serializer = CustomUserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'success',
                 'data': serializer.data
                 })
        return Response({'status': 'failed',
                         'errors': serializer.data
                         }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        operation_id="partial_update_profile",
        summary="Partial Profile Update",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def patch(self, request):
        """Partially update user profile."""
        serializer = CustomUserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': 'success',
                 'data': serializer.data
                 }
            )
        return Response({'status': 'failed',
                         'errors': serializer.data
                         }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Change user password."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [RequireAPIKey, IsAuthenticated]

    @extend_schema(
        operation_id="update_password",
        summary="Change Password",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def post(self, request):
        """Allows an authenticated user to change their password"""
        serializer = ChangePasswordSerializer(
            request.user,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        return Response({'status': 'failed',
                         'errors': serializer.errors
                         }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    serializer_class = None
    permission_classes = [RequireAPIKey, IsAuthenticated]
    @extend_schema(
        operation_id="logout",
        summary="Logout",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            404: helpers.NotFoundErrorSerializer,
            409: helpers.ConflictErrorSerializer,
            429: helpers.RateLimitErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def post(self, request):
        """
            Logout / revoke refresh token (optional, recommended).

            Invalidates the refresh token server-side. Access tokens
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
                'status': 'success',
                'message': 'Successfully logged out.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'failed',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
