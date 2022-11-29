from config import switch_profile, CurrentProfileNotFound, get_all_profiles


def profile_command(key: str):
    try:
        switch_profile(key)
        print(f"Switch to profile {key} successful")
    except CurrentProfileNotFound:
        print(f"Profile with key {key} not found")
        print(f"Profiles found: {', '.join(get_all_profiles())}")
