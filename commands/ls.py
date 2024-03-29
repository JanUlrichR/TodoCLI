import json
from datetime import datetime
from typing import List

from rich.console import Console
from rich.table import Table

from config import load_current_profile, CurrentProfileNotFound, get_current_key
from issue import Priority
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


def get_text(x):
    # Easier to ask for forgiveness than permission
    try:
        return x["content"][0]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return ""


fields_config = {
    "summary": [titleize, ident],
    "priority": [titleize, lambda x: x['name']],
    "description": [titleize, get_text],
    # "created": [titleize, pretty_date],
    "labels": [titleize, labelize],
    "duedate": [lambda x: "Due Date", pretty_date],
    "status": [titleize, lambda x: ":white_heavy_check_mark:" if x["name"] != "To Do" else ":white_large_square:"]
}


def pretty_print_issues(title, issues, fields):
    table = Table(title=title, padding=1, collapse_padding=True)
    table.add_column("Key")
    for field, [title_function, _] in fields.items():
        justify = "center" if field == "status" else "left"
        table.add_column(title_function(field), justify=justify)

    for issue in issues:
        table.add_row(
            *[issue["key"]] + [data_function(issue["fields"][field]) for field, [_, data_function] in fields.items()])

    console.print(table)


def ls_command(all: bool, priorities: List[Priority], labels: List[str]):
    profile = load_current_profile()
    all_jql_part = ' AND resolution IS EMPTY' if not all else ''
    priorities_jql_part = f' AND priority in ({", ".join(priorities)})' if len(priorities) else ''
    labels_jql_part = "".join([f' AND labels = {label}' for label in labels]) if len(labels) else ''

    jql = f"project = {profile.get_project_key()}{all_jql_part}{priorities_jql_part}{labels_jql_part} ORDER BY priority DESC, duedate ASC"
    ls_command_by_jql(profile, jql)


def ls_command_by_jql(profile, jql):
    issues = []
    max_results = 15
    start_at = 0
    while (True):
        payload = json.dumps({
            "expand": [
                "names",
                "schema",
                "operations"
            ],
            "jql": jql,
            "maxResults": max_results,
            "fieldsByKeys": False,
            "fields": [*fields_config],
            "startAt": start_at
        })
        status, response = request_jira(profile, "/rest/api/3/search", http_method="POST", payload=payload)
        if status != 200:
            print("Error retrieving the tasks")
            return

        new_issues = response["issues"]
        issues.extend(new_issues)

        if len(new_issues) < max_results:
            break
        start_at = start_at + len(new_issues)

    try:
        pretty_print_issues(profile.project_name, issues, fields_config)
    except CurrentProfileNotFound as e:
        print(e)
