import typer

from commands.admin import admin_command

app = typer.Typer()


@app.command()
def admin(cloud_url: str = typer.Option("https://jan-robens.atlassian.net", prompt="Cloud URL: (e.g. https://jan-robens.atlassian.net)"),
          project_name: str = typer.Option("TodoCli", prompt=True),
          account_name: str = typer.Option(..., prompt=True),
          access_token: str = typer.Option(..., prompt=True, hide_input=True)):
    admin_command(cloud_url, project_name, account_name, access_token)


if __name__ == "__main__":
    app()
