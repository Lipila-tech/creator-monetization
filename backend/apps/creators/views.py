from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.creators.models import CreatorProfile
from apps.creators.serializers import CreatorPublicSerializer, CreatorListSerializer


class CreatorPublicView(APIView):
    """API view to retrieve public creator profile data."""
    permission_classes = [AllowAny]

    def get(self, request, slug: str) -> Response:
        """
        Retrieve a public creator profile by slug.
        ---
        parameters:
          - name: slug
            in: path
            required: true
            description: The slug of the creator profile.
            type: string
        responses:
          200:
            description: Successful retrieval of creator profile.
            schema:
              {
              "status": "success",
              "data": {
                  "user": {
                      "id": 1,
                      "username": "creator_username",
                      "full_name": "Creator Full Name",
                      "slug": "creator-slug",
                      "email": "creator@example.com"
                  },
                  "bio": "This is a test bio.",
                  "profile_image": "http://example.com/media/profile_images/image.jpg",
                  "cover_image": "http://example.com/media/cover_images/image.jpg",
                  "website": "http://creatorwebsite.com",
                  "followers_count": 150,
                  "rating": 4.5,
                  "verified": true,
                  "status": "active",
                  "created_at": "2024-01-01T12:00:00Z",
                  "updated_at": "2024-01-02T12:00:00Z
                }
              }
          404:
            "status": "error",
            "message": "Creator profile not found."
        """
        try:
            creator_profile = CreatorProfile.objects.get(user__slug__iexact=slug, status="active")
        except CreatorProfile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Creator profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CreatorPublicSerializer(creator_profile)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class CreatorsListView(APIView):
    """API view to list all active creator profiles."""
    permission_classes = [AllowAny]

    def get(self, request) -> Response:
        """
        Retrieve a list of all active creator profiles.
        ---
        responses:
          200:
            description: Successful retrieval of creator profiles list.
            schema:
              {
              "status": "success",
              "data": [
                  {
                      "user": 1,
                      "bio": "This is a test bio.",
                      "profile_image": "http://example.com/media/profile_images/image.jpg",
                      "cover_image": "http://example.com/media/cover_images/image.jpg",
                      "website": "http://creatorwebsite.com",
                      "followers_count": 150,
                      "rating": 4.5,
                      "verified": true,
                      "created_at": "2024-01-01T12:00:00Z",
                      "updated_at": "2024-01-02T12:00:00Z"
                  },
                  ...
                ]
              }
        """
        creator_profiles = CreatorProfile.objects.filter(status="active").order_by('-followers_count')
        serializer = CreatorListSerializer(creator_profiles, many=True)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )