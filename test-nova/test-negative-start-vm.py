import pytest
from base import get_token, startup_server

def test_startup_server():
    try:
        token = get_token()
        server_id = "non-existing-id"

        startup_response = startup_server(token, server_id)
        assert startup_response.status_code == 404


    except Exception as e:
        pytest.fail(f"Test failed: {e}")
