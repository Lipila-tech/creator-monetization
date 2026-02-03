"""
Management command to create creator wallets for existing creators with no wallet.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.creators.models import CreatorProfile
from apps.wallets.models import Wallet

User = get_user_model()

class Command(BaseCommand):
    help = 'Create CreatorWallet for existing creators with no wallet'

    def handle(self, *args, **options):
        creators = CreatorProfile.objects.select_related('user').filter(user__user_type='creator')
        created_count = 0

        for creator in creators:
            if not hasattr(creator, 'wallet'):
                Wallet.objects.create(creator=creator)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created CreatorWallet for user: {creator.user.username}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Total CreatorWallets created: {created_count}')
        )