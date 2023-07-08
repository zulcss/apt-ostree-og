import os
import sys

import click
from rich.console import Console
from apt_ostree.packages import Packages

console = Console()


@click.command(name="install", help="Install a debian pacakge")
@click.pass_context
@click.argument("packages", nargs=-1)
def install(ctxt, packages):
    if os.getuid() != 0:
        console.print("You are not root!")
        sys.exit(1)

    if len(packages) == 0:
        console.print("You mus specify at least one package")
        sys.exit(1)

    Packages().install(packages)
    """
    workspace_dir = pathlib.Path("/var/tmp/apt-ostree")
    deployment_dir = workspace_dir.joinpath("deployment")

    if not deployment_dir.exists():
        deployment_dir.mkdir(parents=True, exist_ok=True)

    if len(packages) == 0:
        console.print("Please specift at least one packafe")
        sys.exit(1)

    cache = apt_pkg.Cache()

    apt = Apt()
    ostree = Ostree(deployment_dir)

    deployment_dir = ostree.deployment()
    apt.apt_update(deployment_dir)

    pkgs = []
    # Get non-installed packages
    for package in packages:
        pkg = apt.get_package(package)
        if pkg and not pkg.candidate.is_installed:
            pkgs.append(pkg)
        else:
            console.print(f"[red]{package}[/red] is already installed.")
    
        apt.apt_install(deployment_dir, package)

    ostree.post_deployment()
    """
