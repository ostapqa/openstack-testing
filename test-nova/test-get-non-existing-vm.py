from base import get_server_info, get_token
import pytest
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")
server_name = config.get('compute', 'server_name')


def test_get_server_invalid_info():
    try:
        token = get_token()

        server = get_server_info("non-existing-server", token)

        assert server.status_code == 404
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
