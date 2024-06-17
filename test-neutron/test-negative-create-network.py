import allure
import pytest
from base import get_token, create_network

@allure.feature('Neutron')
@allure.story('Create negative network')
def test_negative_create_network():
    try:
        token = get_token()
        network_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        response = create_network(token, network_name)
        assert response.status_code == 400
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
