import pytest
from base import get_token, create_server
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = config.get('compute', 'image')
flavor_id = config.get('compute', 'flavor')
network_id = config.get('compute', 'network')
server_name = config.get('compute', 'server_name')

def test_create_server():
    try:
        token = get_token()

        response = create_server(token, server_name, image_id, flavor_id, network_id)

        assert "id" in response
        assert "self_link" in response
        assert "bookmark_link" in response
        assert "admin_pass" in response
        print(f"Server created successfully: {response['id']}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")