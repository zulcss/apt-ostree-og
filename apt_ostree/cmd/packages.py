"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import os
import sys

from apt_ostree.cmd import options
from apt_ostree.packages.package import Package
from apt_ostree.packages.install import Install
from apt_ostree.packages.uninstall import Uninstall
from apt_ostree.system import check_user
from apt_ostree.utils import run_command
import click
from rich.console import Console

console = Console()
pkg = Package()

@click.group(help='Query debain package information in a deployment')
@click.pass_context
def package(ctxt):
    check_user()

@click.command(name="install", help="Install a debian package")
@click.pass_context
@click.argument("packages", nargs=-1)
def package_install(ctxt, packages):
    package_check(packages)
    pkg.package_install(packages)
    ask_reboot()

@click.command(name="uninstall", help="Uninstall a debian dpackage")
@click.pass_context
@click.argument("packages", nargs=-1)
def package_uninstall(ctxt, packages):
    #package_check(packages)
    pkg.package_uninstall(packages)
    #ask_reboot()

@click.command(name="upgrade", help="Upgrade all packages in a deployment")
@click.pass_context
def package_upgrade(ctxt):
    pkg.package_upgrade()

package.add_command(package_install)
package.add_command(package_uninstall)
package.add_command(package_upgrade)

def package_check(packages):
    if len(packages) == 0:
        console.print("You must specify at least one package")
        sys.exit(1)

def ask_reboot():
    console.print("Don't forget to reboot for changes to take affect!")
    if click.confirm("Do you want to reboot now?"):
        run_command(["shutdown", "-r", "now"])
    else:
        sys.exit(1)
