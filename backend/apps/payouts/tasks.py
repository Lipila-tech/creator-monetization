from celery import shared_task
from apps.wallets.models import Wallet
from apps.payments.services.payout_orchestrator import PayoutOrchestrator


@shared_task
def auto_payout_wallets():
    for wallet in Wallet.objects.filter(balance__gt=0):
        PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=None,  # System initiated
        )
