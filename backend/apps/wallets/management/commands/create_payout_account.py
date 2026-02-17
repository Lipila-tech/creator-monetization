"""
Management command to create payout account associated with wallet with no payout account.
"""

from django.core.management.base import BaseCommand
from apps.wallets.models import Wallet, WalletPayoutAccount

class Command(BaseCommand):
    help = 'Create WalletPayoutAccount for existing wallets with payout account'

    def handle(self, *args, **options):
        wallets = Wallet.objects.filter()
        created_count = 0

        for wallet in wallets:
            if not hasattr(wallet, 'payout_account'):
                WalletPayoutAccount.objects.create(wallet=wallet)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created WalletPayoutAccount for wallet: {wallet.creator}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Total WalletPayoutAccounts created: {created_count}')
        )