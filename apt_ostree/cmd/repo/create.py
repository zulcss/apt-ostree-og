import sys

import click
from rich.console import Console

from apt_ostree import constants
from apt_ostree.cmd import options
from apt_ostree.repo import Repo
from apt_ostree.system import check_user

console = Console()

@click.command(help="Create a debian repository")
@click.pass_context
@options.repo
@options.suite
@click.option(
    "-P", "--pocket",
    help="Pocket to create",
    default="starlingx-updates"
)
def create(ctxt, repo, suite, pocket):
    if suite not in constants.SUITES:
        console.print(f"{suite} is not a valid suite")
        sys.exit(1)

    Repo(repo).create_repo(suite, pocket)
