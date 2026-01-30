from rest_framework import serializers
from apps.creators.models import CreatorProfile
from apps.customauth.serializers import UserSerializer

class CreatorPublicSerializer(serializers.ModelSerializer):
    """Serializer for public creator profile data."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = CreatorProfile
        fields = [
            'user',
            'bio',
            'profile_image',
            'cover_image',
            'website',
            'followers_count',
            'rating',
            'verified',
            'created_at',
            'updated_at',
            'status',
        ]


class CreatorListSerializer(serializers.ModelSerializer):
    """Serializer for listing creator profiles."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CreatorProfile
        fields = [
            'user',
            'bio',
            'profile_image',
            'website',
            'followers_count',
            'rating',
            'verified',
            'created_at',
            'updated_at',
        ]