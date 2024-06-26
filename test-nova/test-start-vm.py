import allure
import pytest
import time

from base import (get_token, create_server, delete_server, image_id, flavor_id,
                  network_id, shutdown_server, get_server_status, startup_server)


@allure.feature('Nova')
@allure.story('Startup a server')
def test_startup_server():
    try:
        token = get_token()
        server_name = "test-server"

        create_response = create_server(token, server_name, image_id, flavor_id, network_id)
        assert create_response.status_code == 202
        server_id = create_response.json().get("server", {}).get("id")
        assert server_id is not None

        time.sleep(10)

        shutdown_response = shutdown_server(token, server_id)
        assert shutdown_response.status_code == 202

        timeout = 200
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = get_server_status(token, server_id)
            if status == "SHUTOFF":
                print(f"Server {server_name} successfully shut down.")
                break

        startup_response = startup_server(token, server_id)
        assert startup_response.status_code == 202

        timeout = 200
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = get_server_status(token, server_id)
            if status == "ACTIVE":
                print(f"Server {server_name} successfully started.")
                break

        deleted_response = delete_server(token, server_id).status_code
        assert deleted_response == 204

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
