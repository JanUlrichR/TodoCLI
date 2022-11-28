import requests
from requests.auth import HTTPBasicAuth
import json

from config import Profile


class ProjectAlreadyExists(Exception):
    pass


def request_jira(profile, rest_url, http_method="GET", payload=None):
    return request_jira_raw(profile.base_url, rest_url, profile.account_name, profile.access_token, http_method,
                            payload)


def request_jira_raw(base_url, rest_url, username, token, http_method="GET", payload=None):
    url = f"{base_url}{rest_url}"

    auth = HTTPBasicAuth(username, token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = requests.request(
            http_method,
            url,
            headers=headers,
            auth=auth,
            data=payload
        )
        return response.status_code, json.loads(response.text) if response.text else {}
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    return 400, None


def create_issue(profile: Profile, payload):
    return create_issue_raw(profile.base_url, profile.account_name, profile.access_token, payload)


def create_issue_raw(base_url, username, token, payload):
    url = f"{base_url}/rest/api/3/issue"

    auth = HTTPBasicAuth(username, token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
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
        "text": "Automatically created by TodoCLI",
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
