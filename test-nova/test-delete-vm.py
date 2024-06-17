import allure
import pytest
from base import (get_token, create_server, image_id, flavor_id,
                  network_id, delete_server_by_name)

@allure.feature('Nova')
@allure.story('Delete server')
def test_delete_server():
    try:
        token = get_token()
        server_name = 'test-server'

        server = create_server(token, server_name, image_id, flavor_id, network_id)
        assert server.status_code == 202
        delete_server_by_name(server_name, token)
    except Exception as e:
        pytest.fail(f"Failed to delete server : {e}")
