from config import load_profile, CurrentProfileNotFound


def open_command():
    try:
        profile = load_profile()
        return f"{profile.base_url}/jira/core/projects/{profile.get_project_key()}/board"
    except CurrentProfileNotFound as e:
        print(e)
