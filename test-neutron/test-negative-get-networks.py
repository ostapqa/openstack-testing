import pytest

from base import get_network_list, get_token


def test_get_network_list():
    try:
        token = get_token() + "additional_invalid_token_data"
        response = get_network_list(token, negative=True)

        assert response.status_code == 401
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
