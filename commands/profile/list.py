from config import get_all_profiles


def profile_list_command():
    print(f"Profiles: {', '.join(get_all_profiles())}")
