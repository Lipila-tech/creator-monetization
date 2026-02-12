from celery import shared_task
from apps.payments.models import Payment
from apps.wallets.models import Wallet
from apps.payments.services.payout_orchestrator import PayoutOrchestrator
from apps.payments.webhooks import resend_callback


@shared_task(bind=True, max_retries=5, default_retry_delay=300)
def resend_deposit_callback(self, payment_id):
    try:
        payment = Payment.objects.filter(id=payment_id).first()

        if not payment:
            return "No Payment Found"

        data, code = resend_callback(payment.id)

        if code != 200:
            raise Exception("Retry")

        return "Callback resent"

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def resend_pending_deposits():
    pending = Payment.objects.filter(
        status__in=["pending", "accepted", "submitted", "processing", "in_reconciliation"]
    )

    for payment in pending:
        resend_deposit_callback.delay(payment.id)
