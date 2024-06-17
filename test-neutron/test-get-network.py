import pytest

from base import get_token, get_network_info, create_network, delete_network


def test_get_network():
    try:
        token = get_token()

        network_name = 'test-network'
        response = create_network(token, network_name)
        network_id = response.json().get("network", {}).get("id")
        assert response.status_code == 201

        get_response = get_network_info(token, network_id)
        assert get_response.status_code == 200
        assert get_response.json()["network"]["name"] == network_name

        delete_response = delete_network(token, network_id)
        assert delete_response.status_code == 204

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
