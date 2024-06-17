import pytest
from base import get_token, get_image_info, update_image_properties, image_id

def test_update_image_properties():
    try:
        token = get_token()

        new_image_name = "updated-test-image"

        new_properties = {
            "name": new_image_name
        }

        update_response = update_image_properties(token, image_id, new_properties)
        assert update_response.status_code == 200

        updated_image_info = get_image_info(image_id, token)
        assert updated_image_info.status_code == 200
        updated_image_data = updated_image_info.json()

        assert updated_image_data["name"] == new_image_name

        previous_name = {
            "name": "ubuntu"
        }

        update_response = update_image_properties(token, image_id, previous_name)
        assert update_response.status_code == 200

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
