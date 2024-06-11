import pytest
from base import get_server_info, get_token, update_server_properties
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

server_name = config.get('compute', 'server_name')


def test_update_server_properties():
    try:
        token = get_token()
        new_server_name = "updated-test-server1"  # новое имя для виртуальной машины

        # Получение информации о виртуальной машине по имени
        server_info = get_server_info(server_name, token)
        server_id = server_info["id"]

        # Обновление свойств виртуальной машины (изменение имени)
        new_properties = {
            "name": new_server_name
        }
        update_server_properties(token, server_id, new_properties)

        # Проверка успешного обновления свойств
        updated_server_info = get_server_info(new_server_name, token)
        assert updated_server_info["name"] == new_server_name
        print(f"Server properties updated successfully: {updated_server_info}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
