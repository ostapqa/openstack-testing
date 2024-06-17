import allure
from base import get_server_info, get_token
import pytest


@allure.feature('Nova')
@allure.story('Negative get server')
def test_get_server_invalid_info():
    try:
        token = get_token()
        server = get_server_info(token, "non-existing-server")

        assert server.status_code == 404
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
