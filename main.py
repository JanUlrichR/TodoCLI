from datetime import datetime
from typing import List, Optional

import typer

from cli_prepocessing import transform_labels
from commands.add import add_command
from commands.delete import delete_command
from commands.edit import edit_command
from commands.finish import finish_command
from commands.ls import ls_command
from commands.open import open_command
from commands.profile.create import profile_create_command
from commands.profile.delete import profile_delete_command
from commands.profile.list import profile_list_command
from commands.profile.reset_password import profile_reset_token_command
from commands.profile.switch import profile_switch_command
from issue import Priority

app = typer.Typer()


@app.command()
def open(keys: List[str] = typer.Option([], "--key", "-k",
                                        help="Todos to open, if no key provided board will be opened")):
    """
    Open board or todo in jira
    """
    urls = open_command(keys)
    for url in urls:
        typer.launch(url)


@app.command()
def ls(priorities: List[Priority] = typer.Option([], "--priority", "-p", case_sensitive=False,
                                                 help="Filter for some priorities"),
       all: bool = typer.Option(False, "--all", "-a", help="Show all, even closed, todo's"),
       labels: List[str] = typer.Option([], "--label", "-l", help="Todos needs to have this label")
       ):
    """
    Listing a (subset of) todos
    """
    ls_command(all, priorities, transform_labels(labels))


@app.command()
def add(summary: str,
        text: str,
        priority: Priority = typer.Option(Priority.medium, "--priority", "-p", case_sensitive=False),
        labels: List[str] = typer.Option([], "--label", "-l"),
        due_date: datetime = typer.Option(None, "--due", "-d", formats=["%d-%m-%Y", "%d-%m-%y", "%d-%m"])):
    """
    Add a new todo
    """
    add_command(summary, text, priority, transform_labels(labels), due_date)


@app.command()
def edit(key: str,
         summary: Optional[str] = typer.Option(None, "--summary", "-s"),
         text: Optional[str] = typer.Option(None, "--text", "-t"),
         priority: Optional[Priority] = typer.Option(None, "--priority", "-p", case_sensitive=False),
         add_labels: List[str] = typer.Option([], "--label-a", "-la"),
         delete_labels: List[str] = typer.Option([], "--label-d", "-ld"),
         due_date: Optional[datetime] = typer.Option(None, "--due", "-d", formats=["%d-%m-%Y", "%d-%m-%y", "%d-%m"])):
    """
    Partially editing a todo
    """
    edit_command(key, summary, text, priority, transform_labels(add_labels), transform_labels(delete_labels), due_date)


@app.command()
def close(key: str, reason: Optional[str] = typer.Argument(None)):
    """
    Closing the todo if it is finished
    """
    finish(key, reason)


@app.command()
def finish(key: str, reason: Optional[str] = typer.Argument(None)):
    """
    Closing the todo if it is finished
    """
    finish_command(key, reason)


@app.command()
def delete(key: str):
    """
    Deleting the todo
    """
    delete_command(key)


profile_app = typer.Typer()
app.add_typer(profile_app, name="profile", help="Manage profiles of this cli tool")


@profile_app.command()
def switch(key: str):
    """
    Switching between profiles
    """
    profile_switch_command(key)


@profile_app.command()
def create(cloud_url: str = typer.Option("https://jan-robens.atlassian.net",
                                         prompt="Cloud URL: (e.g. https://jan-robens.atlassian.net)"),
           project_name: str = typer.Option("TodoCli", prompt=True),
           account_name: str = typer.Option(..., prompt=True),
           access_token: str = typer.Option(..., prompt=True, hide_input=True),
           already_exists: bool = typer.Option([], "--exists", "-e")):
    """
    Creating new profiles and switch to the new profile
    """
    profile_create_command(cloud_url, project_name, account_name, access_token, already_exists)


@profile_app.command(name="list")
def list_command():
    """
    List all profiles
    """
    profile_list_command()


@profile_app.command(name="reset")
def reset_password_command(project_name: str = typer.Option("TodoCli", prompt=True),
                           access_token: str = typer.Option(..., prompt=True, hide_input=True)):
    """
    Reset Token profiles
    """

    profile_reset_token_command(project_name, access_token)


@profile_app.command(name="delete")
def profile_delete(project_name: str = typer.Option("TodoCli", prompt=True),
                   sure: bool = typer.Option("Are you sure ", prompt=True)):
    """
    Delete profiles
    """

    profile_delete_command(project_name, sure)


if __name__ == "__main__":
    app()
