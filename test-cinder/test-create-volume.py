import pytest
from base import get_token, create_volume, delete_volume


def test_create_volume():
    try:
        token = get_token()
        volume_name = "test-volume"
        volume_size = 1
        volume_description = "Test volume description"

        response = create_volume(token, volume_name, volume_size, volume_description)
        volume_id = response.json().get("volume", {}).get("id")
        assert response.status_code == 202

        volume = response.json().get("volume", {})
        assert volume.get("name") == volume_name
        assert volume.get("size") == volume_size
        assert volume.get("description") == volume_description

        delete_volume(token, volume_id)

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
