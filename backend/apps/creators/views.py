from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.creators.models import CreatorProfile
from apps.creators.serializers import (
    CreatorPublicSerializer, CreatorListSerializer,
    UpdateCreatorProfileSerializer, CreatorCategorySerializer, WalletKYCSerializer)
from drf_spectacular.utils import extend_schema
from utils import serializers as helpers
from utils.authentication import RequireAPIKey

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UpdateProfileView(APIView):
    permission_classes = [RequireAPIKey, IsAuthenticated]
    serializer_class = UpdateCreatorProfileSerializer

    @extend_schema(
        operation_id="retrieve_full_profile",
        summary="Retrieve full profile",
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
        """
        Retrieve full profile details for a specific user.

        Returns full profile details including wallet kyc.

        Authentication
        --------------
        Requires authentication (creator).
        """
        serializer = UpdateCreatorProfileSerializer(
            request.user.creator_profile)

        profile_data = serializer.data
        profile_data.update({
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone_number': request.user.phone_number,
            'wallet_kyc': WalletKYCSerializer(
                request.user.creator_profile.wallet.kyc).data
        })
        return Response(
            {"status": "success", "data": profile_data},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        operation_id="update_full_profile",
        summary="Update Full Creator Profile",
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
        """Update current user's full profile information."""

        serializer = UpdateCreatorProfileSerializer(
            instance=request.user.creator_profile,
            data=request.data, partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success"}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class CreatorPublicView(APIView):
    """API view to retrieve public creator profile data."""
    permission_classes = [AllowAny]
    serializer_class = CreatorPublicSerializer

    @extend_schema(
        operation_id="retrieve_creator",
        summary="Retrieve a Creator",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def get(self, request, slug: str) -> Response:
        """
        Retrieve a single public creator profile.

        Returns the public profile information for a creator based on username
        (or creator id). This endpoint powers the public creator page and is
        designed to be shareable.

        Authentication
        --------------
        Public endpoint (no authentication required).

        Path Parameters
        ---------------
        slug : str
            Creator slug
        """
        try:
            creator_profile = CreatorProfile.objects.get(
                user__slug__iexact=slug, status="active")
        except CreatorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Creator profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CreatorPublicSerializer(
            creator_profile, context={'request': request})
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class CreatorsListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CreatorListSerializer

    @extend_schema(
        operation_id="fetch_creators",
        summary="Fetch Active Creators",
        responses={
            200: helpers.SuccessResponseSerializer,
            400: helpers.ValidationErrorSerializer,
            401: helpers.UnauthorizedErrorSerializer,
            403: helpers.ForbiddenErrorSerializer,
            500: helpers.ServerErrorSerializer,
        }
    )
    def get(self, request) -> Response:
        """List active public creators for discovery.

        Returns a paginated list of creators that are publicly visible. Supports
        search and filtering to help patrons discover creators by name, category,
        or tags.

        Authentication
        --------------
        Public endpoint (no authentication required).
        """
        creator_profiles = CreatorProfile.objects.filter(
            status="active").order_by('-followers_count')
        serializer = CreatorListSerializer(
            creator_profiles, many=True, context={'request': request})
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
