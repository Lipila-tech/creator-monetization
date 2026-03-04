import pytest


@pytest.mark.django_db
class TestSelectUserTypeView:
    """Test for selecting user type (creator or patron)"""

    def test_select_user_type(self, auth_api_client, normal_user):
        """Test selecting a user type successfully"""
        auth_api_client.force_authenticate(user=normal_user)
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data
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
            "/api/v1/creators/profile/user-type/", data=data
        )
        assert response.status_code == 400
        assert response.data["error"] == "Invalid data"
        assert "user_type" in response.data["details"]

    def test_select_user_type_unauthenticated(self, auth_api_client):
        """Test that unauthenticated users cannot select a user type"""
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data
        )
        assert response.status_code == 401
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_select_user_type_missing_field(self, auth_api_client, normal_user):
        """Test selecting a user type with missing required field"""
        auth_api_client.force_authenticate(user=normal_user)
        data = {}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data
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
            "/api/v1/creators/profile/user-type/", data=data
        )
        assert response.status_code == 200
        assert response.data["status"] == "success"
        assert response.data["message"] == "User type set to creator."
        normal_user.refresh_from_db()
        assert normal_user.user_type == "creator"

    def test_setting_user_type_to_creator_creates_profile(self, auth_api_client, normal_user):
        """Test that setting user type to creator creates a CreatorProfile"""
        auth_api_client.force_authenticate(user=normal_user)
        data = {"user_type": "creator"}
        response = auth_api_client.post(
            "/api/v1/creators/profile/user-type/", data=data
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.user_type == "creator"
        assert hasattr(normal_user, "creator_profile")
        assert normal_user.creator_profile is not None
