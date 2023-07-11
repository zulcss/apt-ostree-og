"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from . import compose
from . import install
from . import uninstall


@click.group(
    help=f"\nHyrbid images/packages management system."
)
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)


cli.add_command(install.install)
cli.add_command(compose.compose)
cli.add_command(uninstall.uninstall)


def main():
    cli(prog_name="apt-ostree")
