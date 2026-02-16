from rest_framework import serializers
from apps.creators.models import CreatorProfile, CreatorCategory
from apps.customauth.serializers import UserSerializer
from apps.wallets.serializers import WalletKYCSerializer
from apps.wallets.models import Wallet, WalletKYC
from django.db import transaction

from django.contrib.auth import get_user_model

User = get_user_model()


class UpdateCreatorProfileSerializer(serializers.ModelSerializer):
    # --- User fields (writeable passthrough) ---
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    # --- Categories (M2M) ---
    category_slugs = serializers.SlugRelatedField(
        source="categories",
        queryset=CreatorCategory.objects.filter(is_active=True),
        slug_field='slug',
        many=True,
        required=False,
    )
    profile_image = serializers.ImageField(use_url=True, allow_null=True)
    cover_image = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model = CreatorProfile
        fields = [
            # CreatorPatronProfile fields
            "bio",
            "website",
            "profile_image",
            "cover_image",
            
            # User fields
            "first_name",
            "last_name",
            "email",
            "phone_number",
            # M2M
            "category_slugs",
        ]
        extra_kwargs = {
            "bio": {"required": False, "allow_null": True, "allow_blank": True},
            "website": {"required": False, "allow_null": True, "allow_blank": True},
        }


    @transaction.atomic
    def update(self, instance: CreatorProfile, validated_data):
        """
        Update order:
        1) User fields
        2) Profile fields
        3) M2M categories
        """
        # --- pop nested parts ---
        categories = validated_data.pop("categories", None)  # via source="categories"
        
        # --- update User fields (1:1) ---
        user_field_names = ["first_name", "last_name", "email", "phone_number"]
        user_updates = {}
        for f in user_field_names:
            if f in validated_data:
                user_updates[f] = validated_data.pop(f)

        if user_updates:
            user = instance.user
            for k, v in user_updates.items():
                if hasattr(user, k):
                    setattr(user, k, v)
            user.save()
        # --- update profile fields ---
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # --- update categories (M2M) ---
        if categories is not None:
            instance.categories.set(categories)

        return instance

class CreatorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorCategory
        fields = [
            'name',
            'slug',
            'icon',
            'is_featured',
            'country_code',
            'is_active',
        ]


class CreatorPublicSerializer(serializers.ModelSerializer):
    """Serializer for public creator profile data."""
    user = UserSerializer(read_only=True)
    wallet_id = serializers.PrimaryKeyRelatedField(
        source="wallet", read_only=True
    )
    profile_image = serializers.ImageField(max_length=None, use_url=True)
    cover_image = serializers.ImageField(max_length=None, use_url=True)
    categories = CreatorCategorySerializer(many=True, read_only=True)

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
            'categories',
        ]

 
class CreatorListSerializer(serializers.ModelSerializer):
    """Serializer for listing creator profiles."""
    user = UserSerializer(read_only=True)
    profile_image = serializers.ImageField(max_length=None, use_url=True)
    profile_image = serializers.ImageField(max_length=None, use_url=True)
    categories = CreatorCategorySerializer(many=True, read_only=True)
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
            'categories',
        ]
