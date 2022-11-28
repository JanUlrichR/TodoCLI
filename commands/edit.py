import json
from datetime import datetime
from typing import Optional, List

from config import load_profile
from issue import Priority
from jira_helper import request_jira
from util import ensure_key


def edit_command(key: Optional[str],
                 summary: Optional[str],
                 text: Optional[str],
                 priority: Priority,
                 add_labels: List[str],
                 delete_labels: List[str],
                 due_date: Optional[datetime]):
    profile = load_profile()
    prefix_ensured_key = ensure_key(profile, key)
    payload_raw = {}

    if summary or text or priority or due_date:
        payload_raw["fields"] = {}

    if summary:
        payload_raw["fields"]["summary"] = summary

    if text:
        payload_raw["fields"]["description"] = {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{
                    "text": text,
                    "type": "text"
                }]
            }]
        }

    if priority:
        payload_raw["fields"]["priority"] = {
            "id": priority.to_priority_id()
        }

    if due_date:
        if due_date.year == 1900:
            due_date = due_date.replace(year=datetime.today().year)
        payload_raw["fields"]["duedate"] = due_date.strftime("%Y-%m-%d")

    if add_labels or delete_labels:
        payload_raw["update"] = {
            "labels":
                [{"add": label} for label in add_labels] +
                [{"remove": label} for label in delete_labels]
        }

    payload = json.dumps(payload_raw)

    status, response = request_jira(profile, f"/rest/api/3/issue/{prefix_ensured_key}", http_method="PUT",
                                    payload=payload)
    if status == 204:
        print("Todo updated successfully")
    else:
        print("Error when updating todo")
