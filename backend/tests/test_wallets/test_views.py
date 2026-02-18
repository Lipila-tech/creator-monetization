import pytest
from tests.factories import (
    APIClientFactory,
    UserFactory,
    PaymentFactory
    )


@pytest.mark.django_db
class TestWalletPayoutAccountView:
    """Tests for wallet payout account views"""

    def test_only_authorized_frontends_can_access_wallet_payout_account(self, api_client):
        """Test that only authenticated users can access wallet payout account view"""
        response = api_client.get("/api/v1/wallets/payout-account/")
        assert response.status_code == 401

    def test_only_authenticated_users_can_access_wallet_payout_account(self, auth_api_client):
        """Test that only authenticated users can access wallet payout account view"""

        response = auth_api_client.get("/api/v1/wallets/payout-account/")
        assert response.status_code == 401

    def test_get_wallet_payout_account(self, auth_api_client, payout_account_factory):
        """Test getting current user's wallet payout account"""
        auth_api_client.force_authenticate(
            user=payout_account_factory.wallet.creator.user)
        response = auth_api_client.get("/api/v1/wallets/payout-account/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert "account_name" in data
        assert "provider" in data
        assert "phone_number" in data
        assert "verified" in data

    def test_get_wallet_payout_account_no_account(self, auth_api_client, user_factory):
        """Test getting current user's wallet payout account with no account"""
        user_wallet = user_factory.creator_profile.wallet
        user_wallet.payout_account.delete()
        user_wallet.refresh_from_db()
        auth_api_client.force_authenticate(user=user_factory)
        response = auth_api_client.get("/api/v1/wallets/payout-account/")
        assert response.status_code == 404
        assert response.data["status"] == "failed"

    def test_update_wallet_payout_account(self, auth_api_client, payout_account_factory):
        """Test updating current user's wallet payout account"""
        auth_api_client.force_authenticate(
            user=payout_account_factory.wallet.creator.user)
        payload = {
            "accountName": "Updated Creator",
            "phoneNumber": "260964332222",
            "provider": "MTN_MOMO_ZMB",
        }
        response = auth_api_client.put(
            "/api/v1/wallets/payout-account/", data=payload, format='json')
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert data['account_name'] == payload["accountName"]
        assert data['phone_number'] == payload["phoneNumber"]
        assert data['provider'] == payload["provider"]
        assert data['verified'] is False

    def test_update_wallet_payout_account_invalid_provider(self, auth_api_client, payout_account_factory):
        """Test updating current user's wallet payout account with invalid provider"""
        auth_api_client.force_authenticate(
            user=payout_account_factory.wallet.creator.user)
        payload = {
            "accountName": "Updated Bank",
            "phoneNumber": "260964332222",
            "provider": "INVALID_PROVIDER",
        }
        response = auth_api_client.put(
            "/api/v1/wallets/payout-account/", data=payload, format='json')
        assert response.status_code == 400
        assert response.data["status"] == "failed"
        assert "provider" in response.data["errors"]
        

@pytest.mark.django_db
class TestWalletDetailsViews:
    """Tests for wallet views"""
    
    def test_wallet_has_next_payout_date_and_payout_interval(self, api_client, user_factory):
        """Test that wallet details include next payout date"""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user_factory)
        response = api_client.get("/api/v1/wallets/me/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert "next_payout_date" in data
        assert data["next_payout_date"] is not None
        assert "payout_interval_days" in data
        assert data["payout_interval_days"] is not None

    def test_get_user_wallet_404(self, api_client):
        """Test getting a current users wallet with no wallet"""
        user = UserFactory(user_type="admin")
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/wallets/me/")
        assert response.status_code == 404
        assert response.data["status"] == "NOT_FOUND"

    def test_get_user_wallet(self, api_client, user_factory, mocker):
        """Test getting current user's wallet"""
        mock_pawapay = mocker.patch("apps.wallets.views.pawapay_request")
        mock_pawapay.return_value = {"status": "completed"}
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user_factory)
        response = api_client.get("/api/v1/wallets/me/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert "id" in data
        assert "balance" in data
        assert "is_active" in data
        assert "recent_transactions" in data
        assert "cash_in_costs" in data

        # check that pawapay was not called no pending payments
        mock_pawapay.assert_not_called()

    def test_get_user_wallet_with_pending_payment(self, api_client, user_factory, mocker):
        """Test getting current user's wallet with pending payment"""
        mock_pawapay = mocker.patch("apps.wallets.views.pawapay_request")
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        user = user_factory
        payment = PaymentFactory(
            wallet=user.creator_profile.wallet,
            status="pending",
        )
        mock_pawapay.return_value = (
            {"data": {"depositId": str(payment.id), "status": "COMPLETED"}},
            200,
        )
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/wallets/me/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert "id" in data
        assert "balance" in data
        assert "is_active" in data
        assert "currency" in data

        # check that pawapay was called
        mock_pawapay.assert_called()
        # check that payment status was updated
        payment.refresh_from_db()
        assert payment.status == "completed"

    def test_get_wallet_with_multiple_pending_payments(self, api_client, user_factory, mocker):
        """Test getting current user's wallet with multiple pending payments"""
        mock_pawapay = mocker.patch("apps.wallets.views.pawapay_request")
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        user = user_factory
        payments = PaymentFactory.create_batch(
            3,
            wallet=user.creator_profile.wallet,
            status="pending",
        )
        # Mock pawapay to return completed for all payments

        def mock_pawapay_side_effect(method, endpoint, headers=None, payload=None):
            # deposit_id = payload.get("depositId")
            return (
                {"data": {"depositId": "test_id", "status": "COMPLETED"}},
                200,
            )
        mock_pawapay.side_effect = mock_pawapay_side_effect
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/wallets/me/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert "id" in data
        assert "balance" in data
        assert "is_active" in data
        assert "currency" in data

        # check that pawapay was called multiple times
        assert mock_pawapay.call_count == 3
        # check that all payment statuses were updated
        for payment in payments:
            payment.refresh_from_db()
            assert payment.status == "completed"

    def test_get_wallet_transactions(self, api_client, wallet_transaction_factory):
        """Test getting current users tips"""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(
            user=wallet_transaction_factory.wallet.creator.user)
        response = api_client.get("/api/v1/wallets/transactions/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert isinstance(data, list)
        assert len(data) > 0
        transaction = data[0]
        assert "amount" in transaction
        assert "transaction_type" in transaction
        assert "status" in transaction
        assert "reference" in transaction

    def test_get_wallet_with_no_transactions(self, api_client, user_factory):
        """Test getting current user's wallet with no transactions"""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user_factory)
        response = api_client.get("/api/v1/wallets/me/")
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert data.get("recent_transactions") == []


@pytest.mark.django_db
class TestWalletKycView:
    """Tests for wallet KYC view"""

    def test_get_wallet_kyc(self, api_client, user_factory):
        """Test getting current user's wallet KYC"""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user_factory)
        response = api_client.get("/api/v1/wallets/kyc/")
        assert response.status_code == 200
        data = response.data
        assert "id_document_type" in data['data']
        assert "id_document_number" in data['data']
        assert "bank_name" in data['data']
        assert isinstance(data['data']['wallet_id'], str)


    def test_update_wallet_kyc(self, api_client, user_factory):
        """Test updating current user's wallet KYC"""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        api_client.force_authenticate(user=user_factory)
        payload = {
            "idDocumentType": "PASSPORT",
            "idDocumentNumber": "A1234567",
            "accountType": "BANK",
            "bankName": "Updated Bank",
            "bankAccountName": "Updated Account Name",
            "bankAccountNumber": "9876543210",
        }
        response = api_client.put(
            "/api/v1/wallets/kyc/", data=payload, format='json')
        assert response.status_code == 200
        data = response.data.get("data")
        assert data is not None
        assert data["id_document_type"] == payload["idDocumentType"]
        assert data["id_document_number"] == payload["idDocumentNumber"]
        assert data["account_type"] == payload["accountType"]
        assert data["bank_name"] == payload["bankName"]
