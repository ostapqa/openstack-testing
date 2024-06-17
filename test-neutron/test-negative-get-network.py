import pytest

from base import get_token, get_network_info


def test_negative_get_network():
    try:
        token = get_token()
        network = 'non-existing network'

        response = get_network_info(token, network)

        assert response.status_code == 404
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
