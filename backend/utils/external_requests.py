import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Configure file handler for logging errors
if not logger.handlers:
    # Create logs directory if it doesn't exist
    import os

    log_dir = os.path.join(settings.BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    # File handler for error logs
    file_handler = logging.FileHandler(
        os.path.join(log_dir, "pawapay_errors.log"))
    file_handler.setLevel(logging.ERROR)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.ERROR)


def pawapay_request(method, endpoint, headers=None, payload=None):
    """
    Utility function to make requests to PawaPay API.
    Args:
        method: HTTP method as a string (e.g., 'GET', 'POST').
        endpoint: API endpoint string.
        headers: Optional dictionary of headers.
        payload: Optional dictionary for JSON payload.
    Returns:
        Tuple of ({'data': response_data}, status_code).
    """
    url = f"{settings.PAWAPAY_BASE_URL}{endpoint}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.PAWAPAY_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        if method == "POST" and payload is None:
            raise AttributeError("Payload missing")
        response = requests.request(
            method, url, headers=headers, json=payload, timeout=10
        )
        try:
            return response.json(), response.status_code
        except ValueError:
            return response.text, response.status_code
    except AttributeError:
        return {"status": "BAD_REQUEST"}, 400
    except requests.exceptions.RequestException as e:
        logger.error(f"PawaPay Request Error: {e}")
        return {"status": "EXTERNAL_ERROR"}, 500
    except requests.exceptions.ConnectionError:
        return {"status": "NETWORK_ERROR"}, 500

    except Exception as e:
        logger.error(f"Internal Error: {e}")
        return {"status": e}, 500
