import allure
import requests
import configparser

config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)
auth_url = config.get('openstack', 'auth_url')
username = config.get('openstack', 'username')
password = config.get('openstack', 'password')
domain_id = config.get('openstack', 'domain_id')
project_id = config.get('openstack', 'project_id')
project_name = config.get('openstack', 'project_name')
glance_url = config.get('openstack', 'glance_url')
user_domain_name = config.get('openstack', 'user_domain_name')
project_domain_id = config.get('openstack', 'project_domain_id')

flavor_id = config.get('compute', 'flavor')
network_id = config.get('compute', 'network')
image_id = config.get('compute', 'image')
nova_url = config.get('compute', 'nova_url')
cinder_url = config.get('compute', 'cinder_url')
neutron_url = config.get('compute', 'neutron_url')

@allure.step('Get JWT-token')
def get_token():
    url = f"{auth_url}/auth/tokens"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "domain": {
                            "name": user_domain_name
                        },
                        "name": username,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "id": project_id,
                    "domain": {
                        "id": project_domain_id
                    }
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 201:
        token = response.headers.get('X-Subject-Token')
        return token
    else:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")


# nova
@allure.step('Get Server status')
def get_server_status(token, server_id):
    headers = {
        "X-Auth-Token": token
    }
    response = requests.get(f"{nova_url}/{server_id}", headers=headers)
    if response.status_code == 200:
        return response.json()["server"]["status"]
    else:
        raise Exception(f"Failed to get server status. Status code: {response.status_code}, Response: {response.text}")


@allure.step('Create server')
def create_server(token, server_name, image_id, flavor_id, network_id):
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    payload = {
        "server": {
            "name": server_name,
            "imageRef": image_id,
            "flavorRef": flavor_id,
            "networks": [
                {"uuid": network_id}
                ]

        }
    }
    response = requests.post(nova_url, json=payload, headers=headers)
    return response


@allure.step('Delete server')
def delete_server(token, server_id):
    url = f"{nova_url}/{server_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    response = requests.delete(url, headers=headers)
    return response


@allure.step('Delete server by name')
def delete_server_by_name(server_name, token):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }

    url = f"{nova_url}?name={server_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        servers = response.json()["servers"]
        if len(servers) == 0:
            raise Exception(f"No server found with name: {server_name}")
        server_id = servers[0]["id"]
    else:
        raise Exception(f"Failed to get server by name. Status code: {response.status_code}, Response: {response.text}")

    url = f"{nova_url}/{server_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to delete server. Status code: {response.status_code}, Response: {response.text}")


@allure.step('Get server ID by name')
def get_server_id_by_name(server_name, token):
    headers = {
        "Accept": "application/json",
        "User-Agent": "python-novaclient",
        "X-Auth-Token": token,
        "X-OpenStack-Nova-API-Version": "2.1"
    }
    response = requests.get(nova_url, headers=headers)
    if response.status_code == 200:
        servers = response.json()["servers"]
        for server in servers:
            if server["name"] == server_name:
                return server["id"]
    return None


@allure.step('Get server info')
def get_server_info(token, server_id):
    url = f"{nova_url}/{server_id}"
    headers = {
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


@allure.step('Get update server properties')
def update_server_properties(token, server_id, new_properties):
    url = f"{nova_url}/{server_id}"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "server": new_properties
    }
    response = requests.put(url, json=payload, headers=headers)

    return response

@allure.step('Shutdown server')
def shutdown_server(token, server_id):
    url = f"{nova_url}/{server_id}/action"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "os-stop": None
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response


@allure.step('Startup server')
def startup_server(token, server_id):
    url = f"{nova_url}/{server_id}/action"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "os-start": None
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response


@allure.step('Reboot server')
def reboot_server(token, server_id):
    url = f"{nova_url}/{server_id}/action"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "reboot": {
            "type": "SOFT"
        }
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response

# glance
@allure.step('Get image info')
def get_image_info(image_id, token):
    url = f"{glance_url}/images/{image_id}"
    headers = {
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    return response

@allure.step('Get image ID by name')
def get_image_id_by_name(image_name, token):
    url = f"{glance_url}/v2/images"
    headers = {
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        images = response.json()["images"]
        for image in images:
            if image["name"] == image_name:
                return image["id"]
    raise Exception(f"No image found with name: {image_name}")


@allure.step('Update image properties')
def update_image_properties(token, image_id, new_properties):
    url = f"{glance_url}/images/{image_id}"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/openstack-images-v2.1-json-patch"
    }
    payload = [{"op": "replace", "path": f"/{key}", "value": value} for key, value in new_properties.items()]

    response = requests.patch(url, json=payload, headers=headers, verify=False)

    return response


@allure.step('Delete image')
def delete_image(token, image_id):
    url = f"{glance_url}/images/{image_id}"
    headers = {
        "X-Auth-Token": token
    }
    response = requests.delete(url, headers=headers, verify=False)
    return response


@allure.step('Retrieving images')
def list_images(token):
    url = f"{glance_url}/images"
    headers = {
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


# cinder
@allure.step('Create volume')
def create_volume(token, name, size, description=None):
    url = f"{cinder_url}/{project_id}/volumes"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "volume": {
            "name": name,
            "size": size
        }
    }
    if description:
        payload["volume"]["description"] = description

    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response


@allure.step('Get volume info')
def get_volume_info(token, volume_id):
    url = f"{cinder_url}/{project_id}/volumes/{volume_id}"
    headers = {
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


@allure.step('Delete volume')
def delete_volume(token, volume_id):
    url = f"{cinder_url}/{project_id}/volumes/{volume_id}"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers, verify=False)
    return response


@allure.step('Update volume')
def update_volume(token, volume_id, new_name):
    url = f"{cinder_url}/{project_id}/volumes/{volume_id}"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "volume": {
            "name": new_name
        }
    }
    response = requests.put(url, json=payload, headers=headers, verify=False)
    return response


# neutron
@allure.step('Create network')
def create_network(token, network_name):
    url = f"{neutron_url}/networks"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    payload = {
        "network": {
            "name": network_name,
            "admin_state_up": True
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


@allure.step('Get network info')
def get_network_info(token, network_id):
    url = f"{neutron_url}/networks/{network_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    response = requests.get(url, headers=headers)

    return response


@allure.step('Delete network')
def delete_network(token, network_id):
    url = f"{neutron_url}/networks/{network_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    return requests.delete(url, headers=headers)


@allure.step('Get network list')
def get_network_list(token, negative=False):
    url = f"{neutron_url}/networks"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif negative:
        return response

@allure.step('Update network')
def update_network(token, network_id, new_properties):
    url = f"{neutron_url}/networks/{network_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    payload = {
        "network": new_properties
    }

    response = requests.put(url, json=payload, headers=headers)
    return response