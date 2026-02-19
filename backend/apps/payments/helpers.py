from apps.payments.models import PaymentWebhookLog as WebHook
from apps.payments.webhooks import resend_callback

def check_final_status(payment):
    """Checks if the payment is in a final state and logs the webhook call."""
    final_statuses = ["failed", "completed", "reversed"]
    if payment.status in final_statuses:
        # If webhook log already exists for this payment, skip logging
        if not WebHook.objects.filter(external_id=payment.reference).exists():
            WebHook.objects.create(
                parsed_payload={"payment_id": str(payment.id), "status": payment.status},
                event_type=f"deposit.{payment.status}",
                payment=payment,
                provider=payment.provider,
                external_id=payment.reference,
            )
        return payment.status
    else:
        # If not in final state, attempt to resend callback to update status
        data, code = resend_callback(str(payment.id))
        if code == 200:
            return data['status']
        else:
            return payment.status
        