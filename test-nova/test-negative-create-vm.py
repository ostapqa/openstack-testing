import allure
import pytest
from base import get_token, create_server


@allure.feature('Nova')
@allure.story('Negative create server')
def test_create_server():
    try:
        token = get_token()
        image_id = "non-image-id"
        flavor_id = 'non-existing-flavor'
        network_id = 'non-existing-network'
        server_name = "test-server"

        response = create_server(token, server_name, image_id, flavor_id, network_id)

        assert response.status_code == 400
    except Exception as e:
        pytest.fail(f"Test failed: {e}")