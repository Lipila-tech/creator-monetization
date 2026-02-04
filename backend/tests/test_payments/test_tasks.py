import uuid
import pytest
from celery.exceptions import Retry
from apps.payments.models import Payment
from apps.wallets.tasks import (
    resend_deposit_callback,
    resend_pending_deposits,
)


class TestResendDepositCallbackTaskTest:

    def test_resend_callback_success(self, mocker):
        mock_pawapay = mocker.patch("apps.wallets.tasks.pawapay_request")
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            provider="pawapay",
            isp_provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=10,
        )

        mock_pawapay.return_value = ({"status": "ACCEPTED"}, 200)

        result = resend_deposit_callback.run(payment.id)

        assert result == "Callback resent"
        mock_pawapay.assert_called_once_with(
            "POST",
            f"/deposits/resend-callback/{payment.id}",
        )

    def test_resend_callback_retries_on_failure(self, mocker):
        mock_pawapay = mocker.patch("apps.wallets.tasks.pawapay_request")
        mock_retry = mocker.patch("apps.wallets.tasks.resend_deposit_callback.retry")
        payment = Payment.objects.create(
            id=uuid.uuid4(),
            amount=10,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700111111",
            status="PENDING",
        )

        mock_pawapay.return_value = ({}, 500)

        # Celery raises Retry exception internally
        mock_retry.side_effect = Retry()

        with pytest.raises(Retry):
            resend_deposit_callback.run(payment.id)

        mock_retry.assert_called_once()

    def test_resend_callback_no_deposit_id(self, mocker):
        mock_pawapay = mocker.patch("apps.wallets.tasks.pawapay_request")
        deposit_id = uuid.uuid4()
        Payment.objects.create(
            id=deposit_id,
            provider="pawapay",
            isp_provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=10,
        )

        result = resend_deposit_callback.run(None)

        assert result == "No Payment Found"
        mock_pawapay.assert_not_called()


class TestResendPendingDepositsBatchTaskTest:

    def test_resend_pending_deposits_dispatches_tasks(self, mocker):
        mock_delay = mocker.patch("apps.wallets.tasks.resend_deposit_callback.delay")
        p1 = Payment.objects.create(
            id=uuid.uuid4(),
            amount=10,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700000001",
            status="pending",
        )

        p2 = Payment.objects.create(
            id=uuid.uuid4(),
            amount=20,
            provider="AIRTEL_OAPI_ZMB",
            customer_phone="260700000002",
            status="accepted",
        )

        # Should NOT be retried
        Payment.objects.create(
            id=uuid.uuid4(),
            amount=30,
            provider="ZAMTEL_ZMB",
            customer_phone="260700000003",
            status="completed",
        )

        resend_pending_deposits.run()

        assert mock_delay.call_count == 2

        called_ids = {call.args[0] for call in mock_delay.call_args_list}
        assert p1.id in called_ids
        assert p2.id in called_ids

    def test_resend_pending_deposits_no_pending(self, mocker):
        mock_delay = mocker.patch("apps.wallets.tasks.resend_deposit_callback.delay")
        resend_pending_deposits.run()
        mock_delay.assert_not_called()