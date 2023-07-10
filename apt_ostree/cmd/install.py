import os
import sys

import click
from rich.console import Console
from apt_ostree.packages import Packages
from apt_ostree.utils import run_command

console = Console()


@click.command(name="install", help="Install a debian pacakge")
@click.pass_context
@click.argument("packages", nargs=-1)
@click.option("-v", "--verbose", 
              is_flag=True, help="Print more output.")
def install(ctxt, packages, verbose):
    if os.getuid() != 0:
        console.print("You are not root!")
        sys.exit(1)

    if len(packages) == 0:
        console.print("You mus specify at least one package")
        sys.exit(1)

    Packages(verbose).install(packages)

    # Need to reboot to the newer deployment in order to take
    # advantage of the new packages, for now.
    console.print("Don't forget to reboot for changes to take affect!")
    if click.confirm("Do you want to reboot now?"):
        run_command(["shutdown", "-r", "now"])
    else:
        sys.exit(1)

