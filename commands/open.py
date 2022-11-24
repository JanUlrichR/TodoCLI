from typing import List

from config import load_profile, CurrentProfileNotFound


def open_command(keys: List[str]):
    try:
        profile = load_profile()
        if len(keys) == 0:
            return [f"{profile.base_url}/jira/core/projects/{profile.get_project_key()}/board"]
        prefix_ensured_keys = [key if key.startswith(profile.get_project_key()) else f"{profile.get_project_key()}-{key}" for key in keys]
        return [f"{profile.base_url}/browse/{key}" for key in prefix_ensured_keys]
    except CurrentProfileNotFound as e:
        print(e)
