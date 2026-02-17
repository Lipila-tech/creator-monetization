import pytest
from celery.exceptions import Retry
from apps.payments.tasks import (
    resend_deposit_callback,
    resend_pending_deposits,
)
from tests.factories import PaymentFactory
@pytest.mark.django_db
class TestResendDepositCallbackTask:

    def test_resend_callback_success(self, payment_factory, mocker):
        mock_resend = mocker.patch("apps.payments.tasks.resend_callback")
        payment = payment_factory

        mock_resend.return_value = ({"status": "ACCEPTED"}, 200)

        result = resend_deposit_callback.run(str(payment.id))

        assert result == "Callback resent"
        mock_resend.assert_called_once_with(str(payment.id))

    def test_resend_callback_retries_on_failure(self, payment_factory, mocker):
        mock_resend = mocker.patch("apps.payments.tasks.resend_callback")
        mock_retry = mocker.patch("apps.payments.tasks.resend_deposit_callback.retry")
        payment = payment_factory

        mock_resend.return_value = ({}, 500)

        # Celery raises Retry exception internally
        mock_retry.side_effect = Retry()

        with pytest.raises(Retry):
            resend_deposit_callback.run(str(payment.id))

        mock_retry.assert_called_once()

    def test_resend_callback_no_deposit_id(self, mocker):
        mock_resend = mocker.patch("apps.payments.tasks.resend_callback")
        
        result = resend_deposit_callback.run(None)

        assert result == "No Payment Found"
        mock_resend.assert_not_called()

@pytest.mark.django_db
class TestResendPendingDepositsBatchTask:
    from django.db.models.signals import post_save
    import factory

    @factory.django.mute_signals(post_save)
    def test_resend_pending_deposits_dispatches_tasks(self, mocker):
        mock_delay = mocker.patch("apps.payments.tasks.resend_deposit_callback.delay")
        payments = PaymentFactory.create_batch(2)
        resend_pending_deposits.run()

        assert mock_delay.call_count == 2

        called_ids = {call.args[0] for call in mock_delay.call_args_list}
        assert payments[0].id in called_ids
        assert payments[1].id in called_ids

    def test_resend_pending_deposits_no_pending(self, mocker):
        mock_delay = mocker.patch("apps.payments.tasks.resend_deposit_callback.delay")
        resend_pending_deposits.run()
        mock_delay.assert_not_called()