import sys

import click
from rich.console import Console

from apt_ostree import constants
from apt_ostree.repo import Repo
from apt_ostree.system import check_user

console = Console()

@click.command(help="Create a debian repository")
@click.pass_context
@click.option(
    "-R", "--repo",
    help="Path to the repo")
@click.option(
    "-S", "--suite",
    default="bookworm",
    help="Suite to create")
@click.option(
    "-P", "--pocket",
    help="Pocket to create",
    default="starlingx-updates"
)
def create(ctxt, repo, suite, pocket):
    check_user()

    """Make sure repo path exists"""
    if repo is None:
        console.print("You did not specify a path for the repository.")
        sys.exit(1)

    if suite is None:
        console.print("You did not supply a repository, using defaults (bookworm)")
    if suite not in constants.SUITES:
        console.print(f"{suite} is not a valid suite")
        sys.exit(1)

    if pocket is None:
        console.print("You did not supply a pocket, using defaults (starlingx-updates")
        sys.exit(1)

    Repo(repo).create_repo(suite, pocket)
