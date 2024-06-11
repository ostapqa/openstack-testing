from base import get_server_info, get_token
import pytest
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")
server_name = config.get('compute', 'server_name')


def test_get_server_info():
    try:
        token = get_token()

        server = get_server_info(server_name, token)
        server_info = server.json()["server"]

        assert server.status_code is 200
        assert server_info["name"] == server_name
        assert server_info["status"] in ["ACTIVE"]
        print(f"Server info retrieved successfully: {server_info['id']}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
