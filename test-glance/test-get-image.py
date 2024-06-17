import allure
import pytest
from base import get_token, get_image_info, image_id


@allure.feature('Glance')
@allure.story('Get Image Info')
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
