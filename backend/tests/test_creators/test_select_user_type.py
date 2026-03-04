import pytest


@pytest.mark.django_db
class TestSelectUserTypeView:
    """Test for selecting user type (creator or patron)"""

    def test_select_user_type(self, auth_api_client, normal_user):
        """Test selecting a user type successfully"""
        auth_api_client.force_authenticate(user=normal_user)
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data, format='json'
        )
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "User type set to creator."
        normal_user.refresh_from_db()
        assert normal_user.user_type == "creator"

    def test_select_user_type_invalid_choice(self, auth_api_client, normal_user):
        """Test selecting an invalid user type"""
        auth_api_client.force_authenticate(user=normal_user)
        data = {"user_type": "invalid_type"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data, format='json'
        )
        assert response.status_code == 400
        assert response.data["error"] == "Invalid data"
        assert "user_type" in response.data["details"]

    def test_select_user_type_unauthenticated(self, auth_api_client):
        """Test that unauthenticated users cannot select a user type"""
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data, format='json'
        )
        assert response.status_code == 401
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_select_user_type_missing_field(self, auth_api_client, normal_user):
        """Test selecting a user type with missing required field"""
        auth_api_client.force_authenticate(user=normal_user)
        data = {}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data, format='json'
        )
        assert response.status_code == 400
        assert response.data["error"] == "Invalid data"
        assert "user_type" in response.data["details"]

    def test_select_user_type_conflict(self, auth_api_client, normal_user):
        """Test selecting a user type that conflicts with existing type"""
        normal_user.user_type = "creator"
        normal_user.save()
        auth_api_client.force_authenticate(user=normal_user)
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data, format='json'
        )
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "User type set to creator."
        normal_user.refresh_from_db()
        assert normal_user.user_type == "creator"

    def test_setting_user_type_to_creator_triggers_related_signals(self, auth_api_client, normal_user):
        """
        Test that setting user type to creator creates a
        CreatorProfile, Wallet, WalletKyc, and WalletPayoutAccount
        """
        normal_user.user_type = "guest"
        normal_user.save()
        auth_api_client.force_authenticate(user=normal_user)
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data, format='json'
        )
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "User type set to creator."
        normal_user.refresh_from_db()
        assert normal_user.user_type == "creator"
        # Check that CreatorProfile was created
        from apps.creators.models import CreatorProfile
        assert CreatorProfile.objects.filter(user=normal_user).exists()
        creator_profile = CreatorProfile.objects.get(user=normal_user)
        # Check that Wallet was created
        from apps.wallets.models import Wallet, WalletKYC, WalletPayoutAccount
        assert Wallet.objects.filter(creator=creator_profile).exists()
        wallet = Wallet.objects.get(creator=creator_profile)
        # Check that WalletKYC was created
        assert WalletKYC.objects.filter(wallet=wallet).exists()
        # Check that WalletPayoutAccount was created
        assert WalletPayoutAccount.objects.filter(wallet=wallet).exists()
               
