import allure
import pytest
from base import get_token, create_network, update_network, get_network_info, delete_network


@allure.feature('Neutron')
@allure.story('Update network')
def test_update_network():
    try:
        token = get_token()
        network_name = "test-network"
        new_network_name = "updated-network"

        response = create_network(token, network_name)
        assert response.status_code == 201
        network_id = response.json().get("network", {}).get("id")
        assert network_id is not None

        new_properties = {"name": new_network_name}
        update_response = update_network(token, network_id, new_properties)
        assert update_response.status_code == 200

        get_response = get_network_info(token, network_id)
        assert get_response.status_code == 200
        assert get_response.json()["network"]["name"] == new_network_name

        print(f"Network updated successfully: {network_id}")

        delete_response = delete_network(token, network_id)
        assert delete_response.status_code == 204

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
