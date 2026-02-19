import pytest
from apps.payments.helpers import check_final_status

@pytest.mark.django_db
class TestCheckFinalStatus:

    def test_check_final_status(self, payment_factory, mocker):
        # Create a payment in a non-final state
        payment = payment_factory

        # Mock the resend_callback function to return a successful response
        mock_resend = mocker.patch(
            'apps.payments.helpers.resend_callback',
            return_value=({'status': 'completed'}, 200))

        # Call the check_final_status function
        status = check_final_status(payment)

        # Assert that the status is updated to 'completed'
        assert status == 'completed'

        mock_resend.assert_called_once_with(str(payment.id))

    def test_check_final_status_already_final(self, payment_factory, mocker):        
        # Create a payment in a final state
        payment = payment_factory
        payment.status = 'completed'
        payment.save()
        mock_resend = mocker.patch(
            'apps.payments.helpers.resend_callback',
            return_value=({'status': 'completed'}, 200))

        # Call the check_final_status function
        status = check_final_status(payment)

        # Assert that the status remains 'completed'
        assert status == 'completed'

        # Assert that a WebHook log entry is created if it doesn't exist
        from apps.payments.models import PaymentWebhookLog as WebHook
        assert WebHook.objects.filter(
            payment=payment, event_type='deposit.completed').exists()
        mock_resend.assert_not_called()
