import allure
import pytest
from base import (get_token, create_server, image_id, flavor_id,
                  network_id, update_server_properties)

@allure.feature('Nova')
@allure.story('Negative update server properties')
def test_negative_update_server_properties():
    try:
        token = get_token()
        new_server_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        server_name = "test-server"

        create_response = create_server(token, server_name, image_id, flavor_id, network_id)
        assert create_response.status_code == 202
        server_id = create_response.json().get("server", {}).get("id")
        assert server_id is not None

        new_properties = {
            "name": new_server_name
        }
        updated_server_info = update_server_properties(token, server_id, new_properties)

        assert updated_server_info.status_code == 400

        print(f"Server properties updated successfully: {updated_server_info}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
