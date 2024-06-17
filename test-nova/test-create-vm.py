import time

import pytest
from base import get_token, create_server, create_network, get_server_info, \
    delete_server, delete_network
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")


def test_create_server():
    try:
        token = get_token()
        server_name = "test-server"
        image_id = config.get('compute', 'image')
        flavor_id = config.get('compute', 'flavor')
        network_name = "test-network"

        # ЧТО ТО С СЕТЬЮ
        # network_response = create_network(token, network_name)
        # assert network_response.status_code == 201
        # network_id = network_response.json().get("network", {}).get("id")
        # assert network_id is not None

        network_id = "0b2280b3-74ef-4bb0-a72a-88fdfedb0e93"
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