import pytest
from base import get_token, create_volume, update_volume, get_volume_info, delete_volume


def test_update_volume():
    try:
        token = get_token()
        volume_name = "test-volume-to-update"
        new_name = 'new-name'

        response = create_volume(token, volume_name, 1, "Volume for update test")
        assert response.status_code == 202

        volume_id = response.json().get("volume", {}).get("id")
        assert volume_id is not None

        update_response = update_volume(token, volume_id, new_name)
        print(update_response.status_code)
        assert update_response.status_code == 200

        print(update_response.status_code)
        get_response = get_volume_info(token, volume_id)
        assert get_response.status_code == 200

        print(f"Volume updated successfully: {volume_id}")

        delete_volume(token, volume_id)

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
