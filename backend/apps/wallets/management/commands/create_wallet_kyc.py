"""
Management command to create creator walletKYCS for existing creators with no walletKYC.
"""

from django.core.management.base import BaseCommand
from apps.wallets.models import Wallet, WalletKYC

class Command(BaseCommand):
    help = 'Create CreatorWalletKYC for existing creators with no wallet kyc'

    def handle(self, *args, **options):
        wallets = Wallet.objects.filter()
        created_count = 0

        for wallet in wallets:
            if not hasattr(wallet, 'kyc'):
                WalletKYC.objects.create(wallet=wallet)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created WalletKYC for wallet: {wallet.creator}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Total WalletKYCs created: {created_count}')
        )