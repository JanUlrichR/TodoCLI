import json

from rich import print

from config import save_profile, Profile, switch_profile
from jira_helper import create_project, ProjectAlreadyExists, request_jira_raw, request_jira, get_project


def profile_create_command(cloud_url: str, project_name: str, account_name: str, access_token: str,
                           already_exists: bool):
    check_connection_status, check_connection_response = request_jira_raw(cloud_url, "/rest/api/3/myself",
                                                                          account_name, access_token)
    if check_connection_status != 200:
        print("[bold red]Could not connect to your site! Please check the values you entered[/bold red] :boom:")
        return

    project_id = ""
    if not already_exists:
        try:
            _, create_project_response = create_project(project_name, check_connection_response['accountId'], cloud_url,
                                                        account_name, access_token)
            project_id = create_project_response["id"]
        except ProjectAlreadyExists:
            print(
                f"[bold red]Project with name [/bold red][bold yellow]'{project_name}'[/bold yellow][bold red] already exists. Please choose another name or delete this project or use the -e flag[/bold red] :boom:")
    else:
        _, get_project_response = get_project(project_name, cloud_url, account_name, access_token)
        project_id = get_project_response["id"]

    profile = save_profile(Profile(cloud_url, account_name, access_token, project_name, project_id,
                                   check_connection_response['accountId']))
    switch_profile(project_name)
    add_user_as_admin(profile)

    print(f"Successfully set up the project. Happy Planing :white_heavy_check_mark:")


def add_user_as_admin(profile: Profile):
    admin_role_id = get_project_administrator_id(profile)
    payload = json.dumps({
        "user": [
            profile.user_id
        ]
    })

    status, response = request_jira(profile, f"/rest/api/3/project/{profile.get_project_key()}/role/{admin_role_id}",
                                    http_method="POST", payload=payload)


def get_project_administrator_id(profile: Profile):
    status, response = request_jira(profile, f"/rest/api/3/project/{profile.get_project_key()}/role",
                                    http_method="GET")
    if status != 200:
        print("Error retriving project roles")
        return []

    return response["Administrators"][response["Administrators"].rindex("/") + 1:]
