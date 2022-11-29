from config import Profile


def ensure_key(profile: Profile, key: str):
    return key if key.startswith(profile.get_project_key()) else f"{profile.get_project_key()}-{key}"
