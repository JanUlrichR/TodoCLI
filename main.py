from datetime import datetime
from typing import List, Optional

import typer

from commands.add import add_command
from commands.admin import admin_command
from commands.delete import delete_command
from commands.edit import edit_command
from commands.finish import finish_command
from commands.ls import ls_command
from commands.open import open_command
from issue import Priority

app = typer.Typer()


@app.command()
def admin(cloud_url: str = typer.Option("https://jan-robens.atlassian.net",
                                        prompt="Cloud URL: (e.g. https://jan-robens.atlassian.net)"),
          project_name: str = typer.Option("TodoCli", prompt=True),
          account_name: str = typer.Option(..., prompt=True),
          access_token: str = typer.Option(..., prompt=True, hide_input=True)):
    admin_command(cloud_url, project_name, account_name, access_token)


@app.command()
def open(keys: List[str] = typer.Option([], "--key", "-k",
                                        help="Todos to open, if no key provided board will be opened")):
    urls = open_command(keys)
    for url in urls:
        typer.launch(url)


@app.command()
def ls(priorities: List[Priority] = typer.Option([], "--priority", "-p", case_sensitive=False,
                                                 help="Filter for some priorities"),
       all: bool = typer.Option(False, "--all", "-a", help="Show all, even closed, todo's"),
       labels: List[str] = typer.Option([], "--label", "-l", help="Todos needs to have this label")
       ):
    ls_command(all, priorities, labels)


@app.command()
def add(summary: str,
        text: str,
        priority: Priority = typer.Option(Priority.medium, "--priority", "-p", case_sensitive=False),
        labels: List[str] = typer.Option([], "--label", "-l"),
        due_date: datetime = typer.Option(None, "--due", "-d", formats=["%d-%m-%Y", "%d-%m-%y", "%d-%m"])):
    add_command(summary, text, priority, labels, due_date)


@app.command()
def edit(key: str,
         summary: Optional[str] = typer.Option(None, "--summary", "-s"),
         text: Optional[str] = typer.Option(None, "--text", "-t"),
         priority: Optional[Priority] = typer.Option(None, "--priority", "-p", case_sensitive=False),
         add_labels: List[str] = typer.Option([], "--label-a", "-la"),
         delete_labels: List[str] = typer.Option([], "--label-d", "-ld"),
         due_date: Optional[datetime] = typer.Option(None, "--due", "-d", formats=["%d-%m-%Y", "%d-%m-%y", "%d-%m"])):
    edit_command(key, summary, text, priority, add_labels, delete_labels, due_date)


@app.command()
def finish(key: str, reason: Optional[str] = typer.Argument(None)):
    finish_command(key, reason)


@app.command()
def close(key: str, reason: Optional[str] = typer.Argument(None)):
    finish(key, reason)


@app.command()
def delete(key: str):
    delete_command(key)


if __name__ == "__main__":
    app()
