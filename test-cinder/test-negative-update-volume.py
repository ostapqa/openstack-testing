import allure
import pytest
from base import get_token, create_volume, update_volume, delete_volume


@allure.feature('Cinder')
@allure.story('Negative update volume')
def test_update_volume():
    try:
        token = get_token()
        volume_name = "test-volume-to-update"
        new_name = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

        response = create_volume(token, volume_name, 1, "Volume for update test")
        assert response.status_code == 202

        volume_id = response.json().get("volume", {}).get("id")
        assert volume_id is not None

        update_response = update_volume(token, volume_id, new_name)
        print(update_response.status_code)
        assert update_response.status_code == 400

        delete_volume(token, volume_id)

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
