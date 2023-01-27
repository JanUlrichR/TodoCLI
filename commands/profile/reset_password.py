from config import get_all_profiles, load_profile, save_profile


def profile_reset_token_command(project_name: str, access_token: str):

    profile = load_profile(project_name)
    profile.access_token = access_token
    save_profile(profile)
    print(f"Profiles: {', '.join(get_all_profiles())}")
