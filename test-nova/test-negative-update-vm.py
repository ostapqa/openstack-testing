import pytest
from base import get_server_info, get_token, update_server_properties
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

server_name = config.get('compute', 'server_name')


def test_negative_update_server_properties():
    try:
        token = get_token()
        new_server_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        server_info = get_server_info(server_name, token).json()
        server_id = server_info["server"]["id"]

        new_properties = {
            "name": new_server_name
        }
        updated_server_info = update_server_properties(token, server_id, new_properties)

        assert updated_server_info.status_code == 400

        print(f"Server properties updated successfully: {updated_server_info}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
