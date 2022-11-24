from datetime import datetime
from typing import List

import typer

from commands.add import add_command
from commands.admin import admin_command
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
def open():
    url = open_command()
    typer.launch(url)


@app.command()
def ls():
    ls_command()


@app.command()
def add(summary: str,
        description: str,
        priority: Priority = typer.Option(Priority.medium, "--priority", "-p", case_sensitive=False),
        labels: List[str] = typer.Option([], "--label", "-l"),
        due_date: datetime = typer.Option(None, "--due", "-d", formats=["%d-%m-%Y", "%d-%m-%y", "%d-%m"])):
    add_command(summary, description, priority, labels, due_date)


if __name__ == "__main__":
    app()
