import pytest
from base import get_token, get_image_info, update_image_properties
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = config.get('compute', 'image')


def test_update_image_properties():
    try:
        token = get_token()
        new_image_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        new_properties = {
            "name": new_image_name
        }

        update_response = update_image_properties(token, image_id, new_properties)
        assert update_response.status_code == 400


    except Exception as e:
        pytest.fail(f"Test failed: {e}")
