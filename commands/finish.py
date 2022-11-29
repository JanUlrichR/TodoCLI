from config import load_current_profile, Profile
from jira_helper import request_jira
import json
from rich import print

from util import ensure_key


def close_issue(key: str, profile: Profile):
    payload = json.dumps({
        "transition": {
            "id": "21"
        }
    })

    status, response = request_jira(profile, f"/rest/api/3/issue/{key}/transitions", http_method="POST",
                                    payload=payload)
    if status == 400:
        print("Issue could not be transitioned")
    if status == 404:
        print("Key not found or not visible")


def add_comment(key: str, reason: str, profile: Profile):
    payload = json.dumps({
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": reason,
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    })

    status, response = request_jira(profile, f"/rest/api/3/issue/{key}/comment", http_method="POST", payload=payload)
    if status == 404:
        print("Key not found or not visible")
    if status != 201:
        print("Error retrieving the tasks")


def finish_command(key: str, reason: str):
    profile = load_current_profile()

    prefix_ensured_key = ensure_key(profile, key)

    close_issue(prefix_ensured_key, profile)

    if reason:
        add_comment(prefix_ensured_key, reason, profile)
