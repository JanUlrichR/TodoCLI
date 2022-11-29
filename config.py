from dataclasses import dataclass
from os import listdir
from os.path import isfile, join
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
    user_id: str

    def get_project_key(self) -> str:
        return self.project_name[0:9].upper()


class CurrentProfileNotFound(Exception):
    pass


def save_profile(base_url: str, account_name: str, access_token: str, project_name: str, project_id: int,
                 user_id: str) -> Profile:
    return _save_profile(Profile(base_url, account_name, access_token, project_name, project_id, user_id))


def _save_profile(profile: Profile) -> Profile:
    (Path.home() / home_dir_folder_name).mkdir(parents=True, exist_ok=True)

    with (Path.home() / home_dir_folder_name / profile.project_name).open('wb') as profile_file:
        pickle.dump(profile, profile_file)
    return profile


def get_all_profiles():
    path = (Path.home() / home_dir_folder_name)
    return [f for f in listdir(path) if isfile(join(path, f)) and f != current_profile_file_name]


def switch_profile(key: str):
    (Path.home() / home_dir_folder_name).mkdir(parents=True, exist_ok=True)
    if not (Path.home() / home_dir_folder_name / key).exists():
        raise CurrentProfileNotFound
    with (Path.home() / home_dir_folder_name / current_profile_file_name).open('wb') as profile_file:
        pickle.dump(key, profile_file)


def get_current_key() -> str:
    path = (Path.home() / home_dir_folder_name / current_profile_file_name)
    with path.open('rb') as profile_file:
        return pickle.load(profile_file)


def load_current_profile() -> Profile:
    current_key = get_current_key()
    return load_profile(current_key)


def load_profile(key: str) -> Profile:
    path = (Path.home() / home_dir_folder_name / key)

    if not path.exists():
        raise CurrentProfileNotFound

    with path.open('rb') as profile_file:
        return pickle.load(profile_file)
