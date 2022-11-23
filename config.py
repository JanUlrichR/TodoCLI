from dataclasses import dataclass
from pathlib import Path
import pickle

home_dir_folder_name = ".todo_cli"
current_profile_file_name = "current_profile"


@dataclass
class Profile:
    base_url: str
    account_name: str
    access_token: str
    project_name: str
    project_id: int


class CurrentProfileNotFound(Exception):
    pass


def save_profile(base_url: str, account_name: str, access_token: str, project_name: str, project_id: int):
    return _save_profile(Profile(base_url, account_name, access_token, project_name, project_id))


def _save_profile(profile: Profile):
    (Path.home() / home_dir_folder_name).mkdir(parents=True, exist_ok=True)

    with (Path.home() / home_dir_folder_name / current_profile_file_name).open('wb') as profile_file:
        pickle.dump(profile, profile_file)


def load_profile() -> Profile:
    path = (Path.home() / home_dir_folder_name / current_profile_file_name)

    if not path.exists():
        raise CurrentProfileNotFound

    with path.open('rb') as profile_file:
        return pickle.load(profile_file)
