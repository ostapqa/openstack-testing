import time

import pytest
from base import get_token, get_server_info, shutdown_server, get_server_status
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = config.get('compute', 'image')
flavor_id = config.get('compute', 'flavor')
network_id = config.get('compute', 'network')
server_name = config.get('compute', 'server_name')



def test_shutdown_server():
    try:
        token = get_token()
        server_info = get_server_info(server_name, token)
        server_id = server_info.json()["server"]["id"]

        shutdown_response = shutdown_server(token, server_id)
        assert shutdown_response.status_code == 202

        timeout = 300
        poll_interval = 10
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = get_server_status(token, server_id)
            if status == "SHUTOFF":
                print(f"Server {server_name} successfully shut down.")
                return
            time.sleep(poll_interval)

        pytest.fail(f"Server {server_name} was not shut down within the expected time.")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
