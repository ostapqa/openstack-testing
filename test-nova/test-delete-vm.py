import configparser

import pytest
from base import get_token, delete_server_by_name

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")
server_name = "updated-test-server1"

def test_delete_server():
    try:
        token = get_token()

        delete_server_by_name(server_name, token)
    except Exception as e:
        pytest.fail(f"Failed to delete server '{server_name}': {e}")
