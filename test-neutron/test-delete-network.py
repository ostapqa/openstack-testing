import allure
import pytest
from base import get_token, create_network, get_network_info, delete_network


@allure.feature('Neutron')
@allure.story('Get a network')
def test_delete_network():
    try:
        token = get_token()
        network_name = "test-network"

        response = create_network(token, network_name)
        assert response.status_code == 201
        network_id = response.json().get("network", {}).get("id")
        assert network_id is not None

        get_response = get_network_info(token, network_id)
        assert get_response.status_code == 200
        assert get_response.json()["network"]["name"] == network_name

        print(f"Network created successfully: {network_id}")

        delete_response = delete_network(token, network_id)
        assert delete_response.status_code == 204

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
