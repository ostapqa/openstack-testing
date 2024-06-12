import pytest
from base import get_token, create_volume

def test_create_volume():
    try:
        token = get_token()
        volume_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        volume_size = 1
        volume_description = "Test volume description"

        response = create_volume(token, volume_name, volume_size, volume_description)
        assert response.status_code == 400

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
