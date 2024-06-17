import allure
import pytest

from base import get_network_list, get_token


@allure.feature('Neutron')
@allure.story('Get network list')
def test_get_network_list():
    try:
        token = get_token()
        network_list = get_network_list(token)
        assert "networks" in network_list
        assert isinstance(network_list["networks"], list)

        print(f"Network list retrieved successfully: {network_list}")
    except Exception as e:
        pytest.fail(f"Test failed: {e}")
