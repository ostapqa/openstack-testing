import time

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

nova_url = config.get('compute', 'nova_url')


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


def get_server_status(token, server_id):
    headers = {
        "X-Auth-Token": token
    }
    response = requests.get(f"{nova_url}/{server_id}", headers=headers)
    if response.status_code == 200:
        return response.json()["server"]["status"]
    else:
        raise Exception(f"Failed to get server status. Status code: {response.status_code}, Response: {response.text}")


def create_server(token, server_name, image_id, flavor_id, network_id, positive=True):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
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

    if not positive:
        return response

    if response.status_code == 202:
        server_info = response.json()["server"]
        server_id = server_info["id"]

        timeout = 600
        poll_interval = 10
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = get_server_status(token, server_id)
            if status == "ACTIVE":
                server_links = server_info["links"]
                server_self_link = next(link["href"] for link in server_links if link["rel"] == "self")
                server_bookmark_link = next(link["href"] for link in server_links if link["rel"] == "bookmark")
                admin_pass = server_info.get("adminPass", None)
                return {
                    "id": server_id,
                    "self_link": server_self_link,
                    "bookmark_link": server_bookmark_link,
                    "admin_pass": admin_pass
                }
            elif status == "ERROR":
                raise Exception(f"Server creation failed with status: {status}")
            time.sleep(poll_interval)

        raise Exception("Timeout while waiting for server to become ACTIVE")


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


def get_server_info(server_name, token):
    server_id = get_server_id_by_name(server_name, token)
    url = f"{nova_url}/{server_id}"
    headers = {
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    return response


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


def reboot_server(token, server_id):
    url = f"{nova_url}/{server_id}/action"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "reboot": {
            "type": "SOFT"  # Используйте "HARD" для жесткой перезагрузки, если необходимо
        }
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response
