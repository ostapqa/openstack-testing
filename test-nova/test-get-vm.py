import time

from base import get_server_info, get_token, create_server, delete_server
import pytest
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")


def test_get_server_info():
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
        server_id = create_response.json().get("server", {}).get("id")

        time.sleep(10)
        server = get_server_info(token, server_id)
        server_info = server.json()["server"]

        assert server.status_code is 200
        assert server_info["name"] == server_name
        assert server_info["status"] in ["ACTIVE"]
        print(f"Server info retrieved successfully: {server_info['id']}")

        delete_server(token, server_id)
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
