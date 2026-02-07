import pytest
from decimal import Decimal
from apps.payments.models import Payment
from apps.wallets.models import WalletTransaction


@pytest.mark.django_db
class TestCashinViews:

    def test_unautenticated_frontend_client_fails(self, api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)

        data = {
            "patronPhone": "76555555566",
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
            "patronmessage": 'test message'
        }
        response = api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format='json')

        assert response.status_code == 401

    def test_single_deposit_does_not_cashin(self, auth_api_client, wallet_factory, mocker):

        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)

        data = {
            "patronPhone": "7655555556",
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
            "patronmessage": 'test message',
            "patronEmail": "test@email.com",
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 201
        data = response.data
        assert data is not None
        assert data['status'] == 'accepted'

        payments = Payment.objects.filter(wallet=wallet_factory)
        assert payments.count() == 1
        assert payments.first().provider == "MTN_MOMO_ZMB"
        assert payments.first().wallet == wallet_factory

        cashin_tx = WalletTransaction.objects.filter(
            payment=payments.first()).first()
        assert cashin_tx is None

        mock_request.assert_called_once()

    def test_deposit_without_message_accepted(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)

        data = {
            "patronPhone": "7655555556",
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 201
        data = response.data
        assert data is not None
        assert data['status'] == 'accepted'

        payments = Payment.objects.filter(wallet=wallet_factory)
        assert payments.count() == 1
        assert payments.first().provider == "MTN_MOMO_ZMB"

        cashin_tx = WalletTransaction.objects.filter(
            payment=payments.first()).first()
        assert cashin_tx is None

        mock_request.assert_called_once()

    def test_external_gateway_down(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "INTERNAL_ERROR"}, 500)

        data = {
            "patronPhone": "7655555556",
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 503
        mock_request.assert_called_once()

    def test_deposit_no_wallet_exists(self, api_key, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")

        data = {
            "patronPhone": "7655555556",
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
            "patronmessage": 'test message'
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{api_key}/", data, format="json")

        assert response.status_code == 404
        mock_request.assert_not_called()

    def test_deposit_missing_patron_phone_field(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")

        data = {
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
            "patronmessage": 'test message'
        }

        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 400
        data = response.data
        mock_request.assert_not_called()

    def test_deposit_missing_amount_field(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        data = {
            "patronPhone": "7655555556",
            "provider": "MTN_MOMO_ZMB",
            "patronmessage": 'test message'
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 400
        data = response.data
        assert data is not None
        assert data['status'] == 'failed'
        payments = Payment.objects.all()
        assert payments.count() == 0
        assert wallet_factory.balance == 0
        mock_request.assert_not_called()

    def test_deposit_missing_invalid_amount(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        data = {
            "patronPhone": "7655555556",
            "amount": '',
            "provider": "MTN_MOMO_ZMB",
            "patronmessage": 'test message'
        }

        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")
        assert response.status_code == 400
        mock_request.assert_not_called()

    def test_deposit_invalid_amount_type(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        data = {
            "patronPhone": "7655555556",
            "amount": 'one',
            "provider": "MTN_MOMO_ZMB",
            "patronmessage": 'test message'
        }

        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")
        assert response.status_code == 400
        mock_request.assert_not_called()

    def test_deposit_fails_with_invalid_phone_number(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        data = {
            "patronPhone": "invalid-phone",
            "amount": '10',
            "provider": "MTN_MOMO_ZMB",
            "patronmessage": 'test message'
        }

        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 400
        mock_request.assert_not_called()

    def test_deposit_fails_with_null_phone_number(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        data = {
            "patronPhone": "",
            "amount": '10',
            "provider": "MTN_MOMO_ZMB",
            "patronmessage": 'test message'
        }

        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 400
        mock_request.assert_not_called()

    def test_deposit_fails_with_missing_provider_field(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")

        data = {
            "patronPhone": "7655555556",
            "amount": "10",
            "patronmessage": 'test message'
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 400
        mock_request.assert_not_called()

    def test_deposit_fails_with_invalid_provider(self, auth_api_client, wallet_factory, mocker):
        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        data = {
            "patronPhone": "7655555556",
            "provider": 'INVALID_PROVIDER',
            "amount": "10",
            "patronmessage": 'test message'
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 400
        mock_request.assert_not_called()

    def test_deposit_works_with_extra_fields(self, auth_api_client, wallet_factory, mocker):
        """Default DRF behaviour is to drop any unknown fields"""

        mock_request = mocker.patch("apps.payments.views.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)

        data = {
            "patronPhone": "7655555556",
            "provider": "MTN_MOMO_ZMB",
            "amount": "10",
            "patronmessage": 'test message',
            "patronEmail": "test@email.com",
            "extraField": "test",
            "anotherExtraField":""
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")

        assert response.status_code == 201
        data = response.data
        assert data is not None
        assert data['status'] == 'accepted'

  
    def test_payment_with_very_large_amount(self, auth_api_client, wallet_factory, mocker):
        """Test handling of large payment amounts"""
        mock_request = mocker.patch("apps.payments.views.pawapay_request")

        large_amount = 999999.99

        mock_request.return_value = (
            {"depositId": "9999999", "status": "ACCEPTED"},
            200,
        )

        data = {
            "patronPhone": "7655555556",
            "payerEmail": "test@email.com",
            "provider": "MTN_MOMO_ZMB",
            "amount": large_amount,
        }
        response = auth_api_client.post(
            f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")
        assert response.status_code == 201
        payment = Payment.objects.first()
        assert payment.amount == Decimal(str(large_amount))
        mock_request.assert_called_once()

    def test_multiple_tips_to_same_wallet(self, auth_api_client, wallet_factory, mocker):
        """Test handling multiple tips for the same wallet"""
        mock_request = mocker.patch("apps.payments.views.pawapay_request")

        mock_request.return_value = (
            {"depositId": "2000", "status": "ACCEPTED"}, 200)

        for i in range(3):
            data = {
                "patronPhone": "7655555556",
                "provider": "MTN_MOMO_ZMB",
                "amount": str(10 * (i + 1)),
                "patronmessage": 'test message'
            }
            response = auth_api_client.post(
                f"/api/v1/payments/deposits/{wallet_factory.id}/", data, format="json")
            assert response.status_code == 201
        
        mock_request.call_count == 3
        
