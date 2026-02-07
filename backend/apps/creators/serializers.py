from rest_framework import serializers
from apps.creators.models import CreatorProfile
from apps.customauth.serializers import UserSerializer

class CreatorPublicSerializer(serializers.ModelSerializer):
    """Serializer for public creator profile data."""
    user = UserSerializer(read_only=True)
    wallet_id = serializers.PrimaryKeyRelatedField(
        source="wallet", read_only=True
    )
    profile_image = serializers.ImageField(max_length=None, use_url=True)
    cover_image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = CreatorProfile
        fields = [
            'user',
            'wallet_id',
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

    # def get_profile_image(self, obj):
    #     request = self.context.get('request')
    #     if obj.profile_image and request:
    #         return request.build_absolute_uri(obj.profile_image.url)
    #     return None



class CreatorListSerializer(serializers.ModelSerializer):
    """Serializer for listing creator profiles."""
    user = UserSerializer(read_only=True)
    
    profile_image = serializers.ImageField(max_length=None, use_url=True)
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
