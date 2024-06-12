import pytest
from base import get_token, list_images


def test_list_images():
    try:
        token = get_token()

        response = list_images(token)
        assert response.status_code == 200

        images = response.json().get("images", [])
        assert isinstance(images, list)

        if images:
            print(f"Retrieved {len(images)} images.")
        else:
            print("No images found.")

    except Exception as e:
        pytest.fail(f"Test failed: {e}")
