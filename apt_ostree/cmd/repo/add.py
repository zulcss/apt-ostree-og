import sys

import click
from rich.console import Console

from apt_ostree import constants
from apt_ostree.cmd import options
from apt_ostree.repo import Repo
from apt_ostree.system import check_user

console = Console()

@click.command(help="Add a packagedebian repository")
@click.pass_context
@options.repo
@click.option(
    "-s", "--suite",
    help="suite to drop package into",
    default="bookworm"
)
@click.argument("package", nargs=1)
def add(ctxt, repo, suite, package):
    """Make sure repo path exists"""
    if repo is None:
        console.print("You did not specify a path for the repository.")
        sys.exit(1)

    if suite is None:
        console.print("You did not supply a pocket, using defaults (bookworm)")
        sys.exit(1)

    if package is None:
        console.print("You did not supply a pacakge")
        sys.exit(1)

    Repo(repo).add_package(repo, suite, package)
