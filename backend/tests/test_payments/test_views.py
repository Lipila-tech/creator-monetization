import pytest
from decimal import Decimal
from tests.factories import APIClientFactory
from apps.payments.models import Payment
from apps.wallets.models import WalletTransaction

class TestCashinViews:

    @pytest.mark_django_db
    def setup_wallet(self, user_factory):
        wallet = user_factory.creator_profile.wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
        return wallet

    def test_single_deposit_does_not_cashin(self, api_key, auth_api_client, setup_wallet, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
        data = {
                "payerPhone": "765555555",
                "ispProvider": "MTN_MOMO_ZMB",
                "amount": "10",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'pending'

        payment = Payment.objects.filter(wallet=setup_wallet).first()

        cashin_tx = WalletTransaction.objects.filter(payment=payment).first()
        fees = WalletTransaction.objects.filter(
            related_transaction=cashin_tx.first(), transaction_type="FEE"
        )
        assert len(payment) == 1
        assert cashin_tx is None
        assert fees is None
        assert payment.isp_provider == "MTN_MOMO_ZMB"
        assert setup_wallet.balance == 0
        mock_request.assert_called_once()
        
    def test_deposit_without_message_passed(self, api_key, auth_api_client, setup_wallet, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
        
        data = {
                "payerPhone": "765555555",
                "ispProvider": "MTN_MOMO_ZMB",
                "amount": "10",
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'pending'

        payment = Payment.objects.filter(wallet=setup_wallet).first()

        cashin_tx = WalletTransaction.objects.filter(payment=payment).first()
        fees = WalletTransaction.objects.filter(
            related_transaction=cashin_tx.first(), transaction_type="FEE"
        )
        assert len(payment) == 1
        assert cashin_tx is None
        assert fees is None
        assert payment.isp_provider == "MTN_MOMO_ZMB"
        assert setup_wallet.balance == 0
        mock_request.assert_called_once()

    def test_deposit_no_wallet_exists(self, api_key, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
           
        data = {
                "payerPhone": "765555555",
                "ispProvider": "MTN_MOMO_ZMB",
                "amount": "10",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{api_key}", data)

        assert response.status_code == 404
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'WALLET_NOT_FOUND'
        payments = Payment.objects.all()
        assert payments.count() == 0

    def test_deposit_missing_required_field_phone(self, api_key, setup_wallet, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
                
        data = {
                "ispProvider": "MTN_MOMO_ZMB",
                "amount": "10",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'
        payments = Payment.objects.all()
        assert payments.count() == 0
        assert setup_wallet.balance == 0
        mock_request.assert_not_called()

    def test_deposit_missing_required_field_amount(self, api_key, setup_wallet, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
                
        data = {
                "payerPhone": "765555555",
                "ispProvider": "MTN_MOMO_ZMB",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'
        payments = Payment.objects.all()
        assert payments.count() == 0
        assert setup_wallet.balance == 0
        mock_request.assert_not_called()

    def test_deposit_missing_invalid_amount(self, api_key, setup_wallet, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
                  
        data = {
                "payerPhone": "765555555",
                "amount": '',
                "ispProvider": "MTN_MOMO_ZMB",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'
        payments = Payment.objects.all()
        assert payments.count() == 0
        assert setup_wallet.balance == 0
        mock_request.assert_not_called()

    def test_deposit_missing_invalid_phone(self, api_key, setup_wallet, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
                  
        data = {
                "payerPhone": "invalid-phone",
                "amount": '10',
                "ispProvider": "MTN_MOMO_ZMB",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'
        payments = Payment.objects.all()
        assert payments.count() == 0
        assert setup_wallet.balance == 0
        mock_request.assert_not_called()

    def test_deposit_missing_required_field_provider(self, api_key, setup_wallet, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
                 
        data = {
                "payerPhone": "765555555",
                "amount": "10",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'
        
    def test_deposit_fails_with_invalid_provider(self, api_key, setup_wallet, auth_api_client, mocker):
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
               
        data = {
                "payerPhone": "765555555",
                "ispProvider": 'BAD_REQUEST',
                "amount": "10",
                "message": 'test message'
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'
    

    def test_deposit_fails_with_unknown_fields(self, api_key, auth_api_client, setup_wallet, mocker):
        """Tests that a single fee is charged per deposit"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        
            
        data = {
                "payerPhone": "765555555",
                "ispProvider": "MTN_MOMO_ZMB",
                "amount": "10",
                "message": 'test message',
                "extra_field": "extra field"
            }
        # api_client.credentials(HTTP_X_API_KEY=api_key)
        response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)

        assert response.status_code == 400
        data = response.data.get("data")
        assert data is not None
        assert data['status'] == 'BAD_REQUEST'

    
    def test_multiple_tips_to_same_wallet(self, api_key, auth_api_client, setup_wallet, mocker):
        """Test handling multiple tips for the same wallet"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
                
        mock_request.return_value = (
            {"depositId": "2000", "status": "ACCEPTED"}, 200)


        for tip in range(3):
            data = {
                "payerPhone": "765555555",
                "ispProvider": "MTN_MOMO_ZMB",
                "amount": str(10 * (tip + 1)),
                "message": 'test message'
            }
            # api_client.credentials(HTTP_X_API_KEY=api_key)
            response = auth_api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)
            assert response.status_code == 200

        # Verify all tips have associated payments
        payments = Payment.objects.filter(wallet=setup_wallet, status="ACCEPTED")
        assert payments.count() == 3
        mock_request.call_count == 3
        
            
    def test_payment_with_very_large_amount(self, api_key, api_client, setup_wallet, mocker):
        """Test handling of large payment amounts"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        
        large_amount = 999999.99
        
        mock_request.return_value = (
            {"depositId": "9999999", "status": "ACCEPTED"},
            200,
        )

        data = {
            "payerPhone": "765555555",
            "provider": "pawapay",
            "ispProvider": "MTN_MOMO_ZMB",
            "amount": large_amount,
        }
        api_client.credentials(HTTP_X_API_KEY=api_key)
        response = api_client.post(f"/api/v1/payments/deposits/{setup_wallet.id}", data)
        assert response.status_code == 200
        payment = Payment.objects.first()
        assert payment.amount == Decimal(str(large_amount))
        mock_request.assert_called_once()