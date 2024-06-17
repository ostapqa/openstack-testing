import allure
import time
import pytest
from base import (get_token, create_server, delete_server, image_id, flavor_id,
                  network_id, update_server_properties)


@allure.feature('Nova')
@allure.story('Update server properties')
def test_update_server_properties():
    try:
        token = get_token()
        server_name = "test-server"
        new_server_name = "new-server"

        create_response = create_server(token, server_name, image_id, flavor_id, network_id)
        assert create_response.status_code == 202
        server_id = create_response.json().get("server", {}).get("id")
        assert server_id is not None

        time.sleep(10)

        new_properties = {
            "name": new_server_name
        }
        updated_server_info = update_server_properties(token, server_id, new_properties)

        assert updated_server_info.status_code == 200

        print(f"Server properties updated successfully: {updated_server_info}")

        deleted_response = delete_server(token, server_id).status_code
        assert deleted_response == 204

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
