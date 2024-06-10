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


def create_image(token, image_name, image_url):
    url = f"{glance_url}/v2/images"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "name": image_name,
        "disk_format": "qcow2",
        "container_format": "bare",
        "visibility": "public",
        "location": image_url
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to create image: {response.status_code}, {response.text}")
