from config import delete_profile


def profile_delete_command(project_name: str, sure: bool):
    if not sure:
        return

    delete_profile(project_name)
    print(f"Deleted Progfile  {project_name}")
