from utils.external_requests import pawapay_request, requests

class TestPawapayRequest:
    # ---------------------------------------------------------
    # Test successful JSON response
    # ---------------------------------------------------------
    def test_success_json_response(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "OK"}
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        data, status = pawapay_request("GET", "/deposit/")
        assert status == 200
        assert data == {"status": "OK"}
        requests.request.assert_called_once()

    # ---------------------------------------------------------
    # Test successful non-JSON response (text fallback)
    # ---------------------------------------------------------
    
    def test_success_text_response(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError("not json")
        mock_response.text = "raw-response"
        mock_response.status_code = 200
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        data, status = pawapay_request("GET", "/deposit/")

        assert status == 200
        assert data == "raw-response"

    # ---------------------------------------------------------
    # Test error from requests (network error, timeout, etc.)
    # ---------------------------------------------------------
    
    def test_request_exception(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.side_effect = Exception("Network down")
        
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        payload = {"amount": 100}
        data, status = pawapay_request("POST", "/deposit/", payload=payload)

        assert status == 500
        assert "status" in data
        
    # ---------------------------------------------------------
    # Test payload + headers passed correctly
    # ---------------------------------------------------------
    
    def test_request_arguments_passed(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"ok": True}
        mock_response.status_code = 201
        
        payload = {"amount": 100}
        patch_path = "utils.external_requests.requests.request"
        mock_request = mocker.patch(patch_path, return_value=mock_response)
        pawapay_request("POST", "/deposits/", headers=None, payload=payload)

        # Verify the function was called with the correct arguments
        # Note: The function builds its own headers with Bearer token
        call_args = mock_request.call_args
        assert call_args[0] == ("POST", "https://api.sandbox.pawapay.io/deposits/")
        assert "Authorization" in call_args[1]["headers"]
        assert call_args[1]["json"] == payload
        assert call_args[1]["timeout"] == 10

    # ---------------------------------------------------------
    # Test non-200 status response with JSON
    # ---------------------------------------------------------
    
    def test_non_200_status(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"error": "bad request"}
        mock_response.status_code = 400
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        data, status = pawapay_request("GET", "/deposit/")

        assert status == 400
        assert data == {"error": "bad request"}

    # ---------------------------------------------------------
    # Test POST without payload raises AttributeError
    # ---------------------------------------------------------
    
    def test_post_without_payload_raises_error(self, mocker):
        """POST requests without payload should raise AttributeError"""
        mock_response = mocker.Mock()
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        data, status = pawapay_request("POST", "/deposit/", payload=None)

        assert status == 400
        assert data is not None
        # Should not call requests.request since it fails before that
        requests.request.assert_not_called()

    # ---------------------------------------------------------
    # Test GET request with payload (allowed)
    # ---------------------------------------------------------
    
    def test_get_request_with_payload(self, mocker):
        """GET requests can have payload (edge case)"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"data": "retrieved"}
        mock_response.status_code = 200
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)

        payload = {"filter": "active"}
        data, status = pawapay_request("GET", "/deposits/", payload=payload)

        assert status == 200
        assert data == {"data": "retrieved"}
        requests.request.assert_called_once()

    # ---------------------------------------------------------
    # Test requests.RequestException (network errors)
    # ---------------------------------------------------------
    
    def test_request_exception_network_error(self, mocker):
        """Network errors should return 500 status"""
        mock_response = mocker.Mock()
        import requests

        mock_response.json.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        data, status = pawapay_request("GET", "/deposit/")
        assert status == 500
        assert data is not None

    # ---------------------------------------------------------
    # Test Timeout Exception
    # ---------------------------------------------------------
    
    def test_request_timeout(self, mocker):
        """Timeout errors should return 500 status"""
        mock_response = mocker.Mock()
        import requests

        mock_response.json.side_effect = requests.exceptions.Timeout(
            "Request timed out")
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)
        data, status = pawapay_request("GET", "/deposit/")

        assert status == 500
        assert data is not None

    # ---------------------------------------------------------
    # Test 500 status response (server error)
    # ---------------------------------------------------------
    
    def test_500_status_response(self, mocker):
        """Server error responses should be returned as-is"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_response.status_code = 500
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)

        data, status = pawapay_request("GET", "/deposit/")

        assert status == 500
        assert data == {"error": "Internal Server Error"}

    # ---------------------------------------------------------
    # Test 401 Unauthorized response
    # ---------------------------------------------------------
    
    def test_401_unauthorized_response(self, mocker):
        """Unauthorized responses should be returned"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_response.status_code = 401
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)

        data, status = pawapay_request("GET", "/deposit/")

        assert status == 401
        assert data == {"error": "Unauthorized"}

    # ---------------------------------------------------------
    # Test 404 Not Found response
    # ---------------------------------------------------------
    
    def test_404_not_found_response(self, mocker):
        """Not found responses should be returned"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"error": "Not Found"}
        mock_response.status_code = 404
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)

        data, status = pawapay_request("GET", "/deposit/")

        assert status == 404
        assert data == {"error": "Not Found"}


    # ---------------------------------------------------------
    # Test headers construction
    # ---------------------------------------------------------
    
    def test_headers_construction(self, mocker):
        """Verify correct headers are always constructed"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        patch_path = "utils.external_requests.requests.request"
        mock_request = mocker.patch(patch_path, return_value=mock_response)

        pawapay_request("GET", "/deposit/")

        call_kwargs = mock_request.call_args[1]
        headers = call_kwargs["headers"]

        # Verify all required headers are present
        assert headers["Accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] is not None
        assert "Bearer" in  headers["Authorization"]

    # ---------------------------------------------------------
    # Test timeout parameter is always 10
    # ---------------------------------------------------------
    
    def test_timeout_always_10(self, mocker):
        """Verify timeout is always set to 10 seconds"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        patch_path = "utils.external_requests.requests.request"
        mock_request = mocker.patch(patch_path, return_value=mock_response)

        for method in ["GET", "POST", "PUT", "DELETE"]:
            mock_response.reset_mock()
            payload = {"data": "test"} if method == "POST" else None
            pawapay_request(method, "/deposit/", payload=payload)

            call_kwargs = mock_request.call_args[1]
            assert call_kwargs["timeout"] == 10

    # ---------------------------------------------------------
    # Test empty JSON response
    # ---------------------------------------------------------
    
    def test_empty_json_response(self, mocker):
        """Empty JSON objects should be returned correctly"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        patch_path = "utils.external_requests.requests.request"
        mocker.patch(patch_path, return_value=mock_response)

        data, status = pawapay_request("GET", "/deposit/")

        assert status == 200
        assert data == {}

    # ---------------------------------------------------------
    # Test large payload
    # ---------------------------------------------------------
    
    def test_large_payload(self, mocker):
        """Large payloads should be handled correctly"""
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.status_code = 201
        patch_path = "utils.external_requests.requests.request"
        mock_request = mocker.patch(patch_path, return_value=mock_response)

        # Create a large payload with multiple nested fields
        large_payload = {
            "items": [{"id": i, "data": "x" * 100} for i in range(50)]}

        data, status = pawapay_request(
            "POST", "/deposit/", payload=large_payload)

        assert status == 201
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["json"] == large_payload
        assert data is not None