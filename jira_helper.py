import requests
from requests.auth import HTTPBasicAuth
import json


class ProjectAlreadyExists(Exception):
    pass


def request_jira(base_url, rest_url, username, token):
    url = f"{base_url}{rest_url}"

    auth = HTTPBasicAuth(username, token)

    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )
        return response.status_code, json.loads(response.text)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    return 400, None


def create_project(name: str, lead_id: str, base_url: str, username: str, token: str):
    url = f"{base_url}/rest/api/3/project"

    auth = HTTPBasicAuth(username, token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    project_key = name[0:9].upper()

    payload = json.dumps({
        "description": "Automatically created by TodoCLI",
        "leadAccountId": lead_id,
        "url": "https://github.com/JanUlrichR/TodoCLI",
        "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-task-tracking",
        "name": name,
        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "business",
        "key": project_key
    })

    try:
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        if (
                response.status_code == 400 and '"projectName":"A project with that name already exists."' in response.text and f'"projectKey":"Project \'{project_key}\' uses this project key."'):
            raise ProjectAlreadyExists
        return response.status_code, json.loads(response.text)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    return 400, None
