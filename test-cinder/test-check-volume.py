import pytest
from base import get_volume_info, create_volume, get_token


def test_get_volume_info():
    try:
        token = get_token()
        volume_name = "test-volume"

        response = create_volume(token, volume_name, 1, "Test volume description")
        assert response.status_code == 202

        volume_id = response.json().get("volume", {}).get("id")
        assert volume_id is not None

        response = get_volume_info(token, volume_id)
        assert response.status_code == 200

        volume_info = response.json().get("volume", {})
        assert volume_info.get("id") == volume_id
        assert volume_info.get("name") == volume_name

        print(f"Volume info retrieved successfully: {volume_info}")

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
