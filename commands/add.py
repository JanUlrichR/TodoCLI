import json
from datetime import datetime
from typing import List, Optional

from config import load_profile
from issue import Priority
from jira_helper import create_issue


def add_command(summary: str,
                description: str,
                priority: Priority,
                labels: List[str],
                due_date: Optional[datetime]):
    profile = load_profile()

    payload_dict = {
        "fields": {
            "summary": summary,
            "issuetype": {
                "id": "10008"  # TODO get this on setup
            },
            "project": {
                "id": profile.project_id
            },
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": description,
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "priority": {
                "id": priority.to_priority_id()
            },
            "labels": labels,
        }
    }
    if due_date:
        if due_date.year == 1900:
            due_date = due_date.replace(year=datetime.today().year)
        payload_dict["fields"]["duedate"] = due_date.strftime("%Y-%m-%d")

    print(payload_dict)

    payload = json.dumps(payload_dict)
    create_issue(profile, payload)
