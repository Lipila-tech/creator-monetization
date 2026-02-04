import uuid
import pytest
from decimal import Decimal
from django.urls import reverse
from tests.factories import APIClientFactory
from apps.payments.models import Payment
from apps.wallets.models import WalletTransaction, Tier

class TestCashinViews:

    @pytest.mark_django_db
    def setup_wallet(self, user_factory):
        wallet = user_factory.creator_profile.wallet
        return wallet

    def test_single_wallet_txn_fee_created(self,
                                           api_client, user_factory, setup_wallet, mocker):
        """Tests that a single fee is charged per deposit"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        mock_request.return_value = (
            {"depositId": "1234", "status": "ACCEPTED"}, 200)
        wallet = setup_wallet
        wallet.kyc.verified = True
        wallet.kyc.save()
     
        data = {
            "phone": "763456789",
            "provider": "pawapay",
            "ispProvider": "MTN_MOMO_ZMB",
            "amount": "10"
        }
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.post("/api/v1/payments/deposit/",data, args=[user_factory.slug])

        payment = Payment.objects.all().first()

        assert response.status_code == 200

        mock_request.return_value = (
            {"data": {"depositId": str(payment.id), "status": "COMPLETED"}},
            200,
        )

        response = api_client.get("/api/v1/payments/status/", args=[payment.id])
        cashin_tx = WalletTransaction.objects.filter(payment=payment)
        fees = WalletTransaction.objects.filter(
            related_transaction=cashin_tx.first(), transaction_type="FEE"
        )
        assert cashin_tx is None
        assert fees is None

    
    def test_completed_status_updates_wallet_balance(self, api_client, setup_wallet, mocker):
        """Test Deposit Status (updates to completed )"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        deposit_id = uuid.uuid4()

        payment = Payment.objects.create(
            wallet=wallet,
            id=deposit_id,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount="10",
            status="ACCEPTED"
        )

        mock_request.return_value = (
            {"data": {"depositId": str(deposit_id), "status": "COMPLETED"}},
            200,
        )
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.get(
            reverse("/api/v1/payments/status/", args=[deposit_id]))
        assert response.status_code == 200

        # refresh from DB
        payment.refresh_from_db()
        assert payment.status == "completed"
        assert payment.wallet.balance == Decimal("0")
        
    def test_failed_payment_is_not_cashed_in(self, api_client, setup_wallet, mocker):
        """Test failed payment is not added to wallet balance"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=100,
            status="ACCEPTED",
            wallet=wallet,
        )

        mock_request.return_value = (
            {"data": {"depositId": str(deposit_id), "status": "REJECTED"}},
            200,
        )
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.get(
            reverse("lipila:payment_status", args=[deposit_id]))
        assert response.status_code == 200

        # refresh from DB
        payment.refresh_from_db()
        assert payment.status == "rejected"
        assert payment.wallet == wallet
        assert payment.wallet.balance == 0
    
    
    def test_update_is_idempotent(self, api_client, setup_wallet, mocker):
        """Check the the endpoint handles duplicate requests correctly"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=100,
            status="accepted",
            wallet=wallet,
        )

        mock_request.return_value = (
            {"data": {"depositId": str(deposit_id), "status": "COMPLETED"}},
            200,
        )
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        # First request
        response = api_client.get(
            reverse("lipila:payment_status", args=[deposit_id]))
        assert response.status_code == 200

        # Second duplicate request
        response = api_client.get(
            reverse("lipila:payment_status", args=[deposit_id]))
        assert response.status_code == 200

        # refresh from DB
        payment.refresh_from_db()
        assert payment.status == "completed"
        assert payment.wallet == wallet
        assert payment.wallet.balance == Decimal("0")

            
    def test_payment_status_pending(self, api_client, setup_wallet, mocker):
        """Test payment status when still pending"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        deposit_id = uuid.uuid4()
        payment = Payment.objects.create(
            id=deposit_id,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=100,
            status="accepted",
            wallet=wallet,
        )

        mock_request.return_value = (
            {"data": {"depositId": str(deposit_id), "status": "PENDING"}},
            200,
        )
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.get(
            reverse("/api/v1/payments/status/", args=[deposit_id]))

        payment.refresh_from_db()
        assert response.status_code == 200
        assert payment.status == "accepted"

    def test_creator_tiers_list(self, api_client, user_factory):
        """Test a correct tiers are displayed"""
        client = APIClientFactory()
        api_client.credentials(HTTP_X_API_KEY=client.api_key)
        response = api_client.get(
            reverse("/api/v1/payments/tiers/", kwargs={"slug": user_factory.slug})
        )

        assert response.status_code == 200
        assert "user" in response.data
        assert response.data["t1"] == '10'
        assert response.data["t2"] == '25'
        assert response.data["t3"] == ''
        assert response.data["currency"] == "ZMW"

    
    def test_fee_calculation_for_different_amounts(self, api_client, setup_wallet, mocker):
        """Test that fees are correctly calculated
            for different payment amounts
        """
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        deposit_id = uuid.uuid4()

        test_amounts = [100, 500, 1000]
        expected_fees = [3, 15, 30]  # 3% fee

        for amount, expected_fee in zip(test_amounts, expected_fees):
            payment = Payment.objects.create(
                id=deposit_id,
                provider="MTN_MOMO_ZMB",
                customer_phone="260700111222",
                amount=amount,
                status="accepted",
                wallet=wallet,
            )

            mock_request.return_value = (
                {"data":
                 {"depositId": str(deposit_id), "status": "COMPLETED"}},
                200,
            )
            client = APIClientFactory()
            api_client.credentials(HTTP_X_API_KEY=client.api_key)
            response = api_client.get(
                reverse("/api/v1/payments/status/", args=[deposit_id])
            )

            payment.refresh_from_db()
            cashin_tx = WalletTransaction.objects.filter(
                payment=payment, transaction_type="CASH_IN"
            )
            fees = WalletTransaction.objects.filter(
                related_transaction=cashin_tx.first(), transaction_type="FEE"
            )
            assert response.status_code == 200
            assert cashin_tx is None
            assert fees is None

            # Clean up for next iteration
            payment.delete()
            deposit_id = uuid.uuid4()

    
    def test_multiple_tiers_same_customer(self, api_client, setup_wallet, tier_factory, mocker):
        """Test handling multiple tips for the same creator"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        
        mock_request.return_value = (
            {"depositId": "2000", "status": "ACCEPTED"}, 200)

        tiers = []
        tier_factory.create_batch(3)

        for tier in tiers:
            data = {
                "phone": "765555555",
                "provider": "pawapay",
                "ispProvider": "MTN_MOMO_ZMB",
            }
            response = api_client.post(
                "/api/v1/payments/deposit/",  data, args=[tier.id])

            assert response.status_code == 201
            assert Tier.objects.get(id=tier.id).payment is not None
            assert wallet.payments.count() == tiers.index(tier) + 1

        # Verify all tiers have associated payments
        payments = Payment.objects.all()
        assert payments.count() == 3

    
    def test_payment_rejection_does_not_affect_wallet(self, api_client, setup_wallet, mocker):
        """Test that rejected payments don't affect wallet"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        initial_balance = wallet.balance
        deposit_id = uuid.uuid4()

        payment = Payment.objects.create(
            id=deposit_id,
            provider="MTN_MOMO_ZMB",
            customer_phone="260700111222",
            amount=100,
            status="accepted",
            wallet=wallet,
        )

        mock_request.return_value = (
            {"data": {"depositId": str(deposit_id), "status": "REJECTED"}},
            200,
        )

        response = api_client.get(
            reverse("lipila:payment_status", args=[deposit_id]))

        payment.refresh_from_db()
        wallet.refresh_from_db()

        # Verify wallet balance remains unchanged
        assert response.status_code == 200
        assert wallet.balance == initial_balance
        assert payment.status == "rejected"

    
    def test_concurrent_payment_status_updates(self, api_client, setup_wallet, mocker):
        """Test handling multiple payment status checks"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
        deposit_ids = [uuid.uuid4() for _ in range(3)]

        mock_request.return_value = (
            {"data": {
                "depositId": str(deposit_ids[0]), "status": "COMPLETED"}},
            200,
        )

        for deposit_id in deposit_ids:
            Payment.objects.create(
                id=deposit_id,
                provider="MTN_MOMO_ZMB",
                customer_phone="260700111222",
                amount=100,
                status="accepted",
                wallet=wallet,
            )

        # Update all payments
        for i, deposit_id in enumerate(deposit_ids):
            mock_request.return_value = (
                {"data": {
                    "depositId": str(deposit_id), "status": "COMPLETED"}},
                200,
            )

            response = api_client.get(
                reverse("lipila:payment_status", args=[deposit_id])
            )
            assert response.status_code == 200

        # Verify all payments are completed
        completed_payments = Payment.objects.filter(status="completed")
        assert completed_payments.count() == 3

        
    def test_payment_with_very_large_amount(self, api_client, setup_wallet, mocker):
        """Test handling of large payment amounts"""
        mock_request = mocker.patch("apps.payments.views.cashin.pawapay_request")
        wallet = setup_wallet
     

        large_amount = 999999.99
        tier = Tier.objects.create(
            creator=wallet.creator, amount=large_amount, remarks="Large payment"
        )

        mock_request.return_value = (
            {"depositId": "9999999", "status": "ACCEPTED"},
            200,
        )

        data = {
            "phone": "765555555",
            "provider": "pawapay",
            "ispProvider": "MTN_MOMO_ZMB",
        }
        response = api_client.post("/api/v1/payments/deposit/tiers/",data, args=[tier.id])
        assert response.status_code == 201
        payment = Payment.objects.first()
        assert payment.amount == Decimal(str(large_amount))
        assert wallet.payments.count() == 1