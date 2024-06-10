import pytest
from base import get_token, create_image


def test_create_image():
    try:
        token = get_token()
        image_name = "test-image"
        image_url = "http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2"

        response = create_image(token, image_name, image_url)

        assert response["status"] == "active"
        print(f"Image created successfully: {response['id']}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
