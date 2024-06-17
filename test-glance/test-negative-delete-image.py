import allure
import pytest
from base import get_token, delete_image

@allure.feature('Glance')
@allure.story('Negative Test: Delete Image')
def test_negative_delete_image():
    try:
        token = get_token()
        image_id = "non-existing-id"

        delete_response = delete_image(token, image_id)
        assert delete_response.status_code == 404

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
