import time

import pytest
from base import delete_server, get_token, reboot_server, get_server_status, create_server
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")


def test_reboot_server():
    try:
        token = get_token()
        server_name = "test-server"
        image_id = config.get('compute', 'image')
        flavor_id = config.get('compute', 'flavor')
        network_id = config.get('compute', 'network')

        create_response = create_server(token, server_name, image_id, flavor_id, network_id)
        assert create_response.status_code == 202
        server_id = create_response.json().get("server", {}).get("id")
        assert server_id is not None

        time.sleep(10)


        reboot_response = reboot_server(token, server_id)
        assert reboot_response.status_code == 202

        timeout = 300
        poll_interval = 10
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = get_server_status(token, server_id)
            if status == "ACTIVE":
                print(f"Server {server_name} successfully rebooted.")
                break
            elif status == "ERROR":
                pytest.fail(f"Server {server_name} failed to reboot and is in ERROR state.")
                time.sleep(poll_interval)


        deleted_response = delete_server(token, server_id).status_code
        assert deleted_response == 204
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
