import typer

from commands.admin import add_user_as_admin
from config import load_profile
from jira_helper import request_jira
from util import ensure_key


def delete_command(key: str):
    profile = load_profile()

    prefix_ensured_key = ensure_key(profile, key)
    delete_confirmation = typer.confirm(f"Are you sure you want to delete todo with key {prefix_ensured_key}?")
    if not delete_confirmation:
        return

    status, response = request_jira(profile, f"/rest/api/3/issue/{prefix_ensured_key}", http_method="DELETE")

    if status == 400:
        print("Todo has subtasks")
    elif status == 403:
        print("No permissions to delete")
    elif status == 404:
        print("Issue not found")
    else:
        print(f"Deletion of Todo with key {prefix_ensured_key} successful")
