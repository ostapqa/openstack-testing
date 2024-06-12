import pytest
from base import get_image_info, get_token, delete_image
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = config.get('compute', 'image-to-delete')


def test_delete_image():
    try:
        token = get_token()

        delete_response = delete_image(token, image_id)
        assert delete_response.status_code == 204

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
