import pytest
from base import get_token, get_image_info
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = "fake-image-id"

def test_get_image_info():
    try:
        token = get_token()

        image_info = get_image_info(image_id, token)

        assert image_info.status_code == 404
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
