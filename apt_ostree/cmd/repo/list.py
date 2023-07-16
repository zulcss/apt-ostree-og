import sys

import click
from rich.console import Console

from apt_ostree import constants
from apt_ostree.cmd import options
from apt_ostree.repo import Repo
from apt_ostree.system import check_user

console = Console()

@click.command(name="list", help="Create a debian repository")
@click.pass_context
@options.repo
@options.suite
def list_packages(ctxt, repo, suite):
    """Make sure repo path exists"""
    if suite not in constants.SUITES:
        console.print(f"{suite} is not a valid suite")
        sys.exit(1)

    Repo(repo).list_packages(repo, suite)
