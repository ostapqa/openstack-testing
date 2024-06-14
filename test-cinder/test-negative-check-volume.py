import pytest
from base import get_volume_info, create_volume, get_token, delete_volume


def test_get_volume_info():
    try:
        token = get_token()
        volume_id = "non-existing-id"

        response = get_volume_info(token, volume_id)
        assert response.status_code == 404

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
