import allure
import time
import pytest

from base import delete_volume, create_volume, get_token, get_volume_info


@allure.feature('Cinder')
@allure.story('Delete Volume')
def test_delete_volume():
    try:
        token = get_token()
        volume_name = "test-volume-to-delete"

        response = create_volume(token, volume_name, 1, "Volume for deletion test")
        assert response.status_code == 202

        volume_id = response.json().get("volume", {}).get("id")
        assert volume_id is not None

        delete_response = delete_volume(token, volume_id)
        assert delete_response.status_code == 202

        time.sleep(5)
        get_response = get_volume_info(token, volume_id)
        assert get_response.status_code == 404

        print(f"Volume deleted successfully: {volume_id}")

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
