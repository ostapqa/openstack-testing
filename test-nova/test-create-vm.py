import time
import allure
import pytest
from base import (get_token, create_server, get_server_info, delete_server, delete_network, image_id, flavor_id,
                  network_id)

@allure.feature('Nova')
@allure.story('Create server')
def test_create_server():
    try:
        token = get_token()
        server_name = "test-server"
        create_response = create_server(token, server_name, image_id, flavor_id, network_id)
        assert create_response.status_code == 202
        server_id = create_response.json().get("server", {}).get("id")
        assert server_id is not None

        time.sleep(10)
        get_response = get_server_info(token, server_id)
        assert get_response.status_code == 200

        assert get_response.json()["server"]["name"] == server_name

        print(f"Server created successfully: {server_id}")

        delete_response = delete_server(token, server_id)
        assert delete_response.status_code == 204

        delete_network(token, network_id)
    except Exception as e:
        pytest.fail(f"Test failed: {e}")