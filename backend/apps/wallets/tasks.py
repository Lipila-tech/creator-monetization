from celery import shared_task
from utils.external_requests import pawapay_request
from apps.payments.models import Payment
from apps.wallets.models import Wallet
from apps.payments.services.payout_orchestrator import PayoutOrchestrator


@shared_task
def auto_payout_wallets():
    for wallet in Wallet.objects.filter(balance__gt=0):
        PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=None,  # System initiated
        )


@shared_task(bind=True, max_retries=5, default_retry_delay=300)
def resend_deposit_callback(self, payment_id):
    try:
        payment = Payment.objects.filter(id=payment_id).first()

        if not payment:
            return "No Payment Found"

        data, code = pawapay_request(
            "POST", f"/deposits/resend-callback/{payment.id}")

        if code != 200:
            raise Exception("Retry")

        return "Callback resent"

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def resend_pending_deposits():
    pending = Payment.objects.filter(
        status__in=["pending", "accepted", "submitted", "processing"]
    )

    for payment in pending:
        resend_deposit_callback.delay(payment.id)
