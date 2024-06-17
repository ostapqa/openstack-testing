import pytest
from base import get_token, create_network, get_network_info, delete_network


def test_delete_network():
    try:
        token = get_token()
        network_name = "non-existing-network"

        response = delete_network(token, network_name)
        assert response.status_code == 404
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
