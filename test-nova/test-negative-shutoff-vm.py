import pytest
from base import get_token, shutdown_server

def test_negative_shutdown_server():
    try:
        token = get_token()
        server_id = "non-existing-id"

        shutdown_response = shutdown_server(token, server_id)
        assert shutdown_response.status_code == 404

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
