import json
from datetime import datetime

from rich.console import Console
from rich.table import Table

from config import load_profile, CurrentProfileNotFound
from jira_helper import request_jira

import locale

console = Console()


def try_parsing_date(text):
    for fmt in ("%Y-%m-%d", '%Y-%m-%dT%H:%M:%S.%f%z'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


titleize = lambda x: x.capitalize()
ident = lambda x: x if x else ""
locale.setlocale(locale.LC_ALL, "de_DE.utf8")
pretty_date = lambda x: try_parsing_date(x).strftime("%a, %d. %b %Y") if x else ""
labelize = lambda x: ", ".join(x)

def get_description(x):
    # Easier to ask for forgiveness than permission
    try:
        return x["content"][0]["content"][0]["text"]
    except (KeyError, IndexError):
        return ""


fields_config = {
    "summary": [titleize, ident],
    "priority": [titleize, lambda x: x['name']],
    "description": [titleize, get_description],
    #"created": [titleize, pretty_date],
    "labels": [titleize, labelize],
    "duedate": [lambda x: "Due Date", pretty_date],
    "status": [titleize, lambda x: ":white_heavy_check_mark:" if x["name"] != "To Do" else ":white_large_square:"]
}


def pretty_print_issues(issues, fields):
    table = Table(title="Todos", padding=1, collapse_padding=True)
    table.add_column("Key")
    for field, [title_function, _] in fields.items():
        justify = "center" if field == "status" else "left"
        table.add_column(title_function(field), justify=justify)

    for issue in issues:
        table.add_row(
            *[issue["key"]] + [data_function(issue["fields"][field]) for field, [_, data_function] in fields.items()])

    console.print(table)


def ls_command():
    try:
        profile = load_profile()

        jql = f"project = {profile.get_project_key()} ORDER BY priority DESC, duedate ASC"

        payload = json.dumps({
            "expand": [
                "names",
                "schema",
                "operations"
            ],
            "jql": jql,
            "maxResults": 15,
            "fieldsByKeys": False,
            "fields": [*fields_config],
            "startAt": 0
        })
        status, response = request_jira(profile, "/rest/api/3/search", http_method="POST", payload=payload)
        if status != 200:
            print("Error retrieving the tasks")
            return
        pretty_print_issues(response["issues"], fields_config)
    except CurrentProfileNotFound as e:
        print(e)
