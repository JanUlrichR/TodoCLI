from typing import List

from config import load_current_profile, CurrentProfileNotFound
from util import ensure_key


def open_command(keys: List[str]):
    try:
        profile = load_current_profile()
        if len(keys) == 0:
            return [f"{profile.base_url}/jira/core/projects/{profile.get_project_key()}/board"]
        prefix_ensured_keys = [ensure_key(key) for key in keys]
        return [f"{profile.base_url}/browse/{key}" for key in prefix_ensured_keys]
    except CurrentProfileNotFound as e:
        print(e)
