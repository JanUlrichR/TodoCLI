from datetime import datetime
from typing import List, Optional

import typer

from commands.add import add_command
from commands.admin import admin_command
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
        description: str,
        priority: Priority = typer.Option(Priority.medium, "--priority", "-p", case_sensitive=False),
        labels: List[str] = typer.Option([], "--label", "-l"),
        due_date: datetime = typer.Option(None, "--due", "-d", formats=["%d-%m-%Y", "%d-%m-%y", "%d-%m"])):
    add_command(summary, description, priority, labels, due_date)


@app.command()
def finish(key: str, reason: Optional[str] = typer.Argument(None)):
    finish_command(key, reason)

@app.command()
def close(key: str, reason: Optional[str] = typer.Argument(None)):
    finish(key, reason)


if __name__ == "__main__":
    app()
