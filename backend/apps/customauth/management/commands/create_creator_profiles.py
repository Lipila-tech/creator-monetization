"""
Management command to create creator profiles for existing users with user_type 'creator'.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.creators.models import CreatorProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Create CreatorProfile for existing users with user_type "creator"'

    def handle(self, *args, **options):
        creators = User.objects.filter(user_type='creator')
        created_count = 0

        for user in creators:
            if not hasattr(user, 'creator_profile'):
                CreatorProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created CreatorProfile for user: {user.username}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Total CreatorProfiles created: {created_count}')
        )