"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import os
import sys

from apt_ostree.cmd import options
from apt_ostree.packages.install import Install
from apt_ostree.packages.uninstall import Uninstall
from apt_ostree.utils import run_command
import click
from rich.console import Console

console = Console()

@click.group(help='Query debain package information in a deployment')
@click.pass_context
def package(ctxt):
    if os.getuid() != 0:
        console.print("You are not root!")
        sys.exit(1)

@click.command(name="install", help="Install a debian package")
@click.pass_context
@click.argument("packages", nargs=-1)
def package_install(ctxt, packages):
    package_check(packages)
    Install().run(packages)
    ask_reboot()

@click.command(name="uninstall", help="Uninstall a debian dpackage")
@click.pass_context
@click.argument("packages", nargs=-1)
def package_uninstall(ctxt, packages):
    package_check(packages)
    Uninstall().run(packages)
    ask_reboot()

@click.command(name="list", help="List all packages in a deployment")
@click.pass_context
@options.branch
def package_list(ctxt, branch):
    pass

package.add_command(package_list)
package.add_command(package_install)
package.add_command(package_uninstall)

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
