import pytest
from base import get_token, get_image_info
import configparser

config = configparser.ConfigParser()
config.read("/home/ostap/PycharmProjects/openstack-testing/config.ini")

image_id = config.get('compute', 'image')

def test_get_image_info():
    try:
        token = get_token()

        image_info = get_image_info(image_id, token)

        assert image_info.status_code == 200

        image_data = image_info.json()
        assert "id" in image_data
        assert "status" in image_data
        print(f"Image information retrieved successfully: {image_data}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
