from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.creators.models import CreatorProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_creator_profile(sender, instance, created, **kwargs):
    """Create a CreatorProfile when a User with user_type 'creator' is created."""
    if created and instance.user_type == 'creator':
        CreatorProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def update_creator_profile(sender, instance, **kwargs):
    """Ensure that a CreatorProfile exists for users with user_type
    'creator' and delete it if user_type changes."""
    if instance.user_type == 'creator':
        CreatorProfile.objects.get_or_create(user=instance)
    else:
        CreatorProfile.objects.filter(user=instance).delete()