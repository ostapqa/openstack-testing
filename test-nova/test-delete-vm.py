import pytest
from base import create_server, get_token, delete_server_by_name
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = config.get('compute', 'image')
flavor_id = config.get('compute', 'flavor')
network_id = config.get('compute', 'network')


def test_delete_server():
    try:
        token = get_token()
        server_name = 'test-server'
        server = create_server(token, server_name, image_id, flavor_id, network_id)
        delete_server_by_name(server_name, token)
    except Exception as e:
        pytest.fail(f"Failed to delete server '{server_name}': {e}")
