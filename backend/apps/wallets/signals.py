from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.creators.models import CreatorProfile
from apps.wallets.models import Wallet, WalletKYC

@receiver(post_save, sender=CreatorProfile)
def create_wallet_for_creator(sender, instance, created, **kwargs):
    """Create a Wallet when a CreatorProfile is created."""
    if created:
        Wallet.objects.get_or_create(creator=instance)


@receiver(post_save, sender=Wallet)
def create_wallet_kyc_for_wallet(sender, instance, created, **kwargs):
    """Create a WalletKYC when a Wallet is created."""
    if created:
        WalletKYC.objects.get_or_create(wallet=instance)