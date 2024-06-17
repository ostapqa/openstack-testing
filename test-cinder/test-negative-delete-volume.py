import pytest

from base import delete_volume, get_token


def test_delete_volume():
    try:
        token = get_token()

        volume_id = 'fake-volume-id'

        delete_response = delete_volume(token, volume_id)
        assert delete_response.status_code == 404

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
