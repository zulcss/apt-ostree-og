import os
import sys

from apt_ostree.packages.uninstall import Uninstall
import click
from rich.console import Console

console = Console()


@click.command(name="uninstall", help="Uninstall a Debian package")
@click.pass_context
@click.argument("packages", nargs=-1)
@click.option("-v", "--verbose",
              is_flag=True, help="Print more output.")
def uninstall(ctxt, packages, verbose):
    if os.getuid() != 0:
        console.print("You are not root!")
        sys.exit(1)

    if len(packages) == 0:
        console.print("You must specify at least one package")
        sys.exit(1)

    Uninstall(verbose).run(packages)
