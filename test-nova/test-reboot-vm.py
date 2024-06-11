import time

import pytest
from base import get_server_info, get_token, reboot_server, get_server_status
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

server_name = config.get('compute', 'server_name')


def test_reboot_server():
    try:
        token = get_token()

        server_info = get_server_info(server_name, token)
        server_id = server_info.json()["server"]["id"]

        reboot_response = reboot_server(token, server_id)
        assert reboot_response.status_code == 202

        timeout = 300
        poll_interval = 10
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = get_server_status(token, server_id)
            if status == "ACTIVE":
                print(f"Server {server_name} successfully rebooted.")
                return
            elif status == "ERROR":
                pytest.fail(f"Server {server_name} failed to reboot and is in ERROR state.")
            time.sleep(poll_interval)

        pytest.fail(f"Server {server_name} did not reboot within the expected time.")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
