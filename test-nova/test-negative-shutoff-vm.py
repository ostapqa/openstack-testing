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
        assert shutdown_response.status_code == 409

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
