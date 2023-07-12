"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click

from apt_ostree.cmd import options
from apt_ostree.image import Image


@click.command(help="Compose an image")
@click.pass_context
@options.config
def image(ctxt, config):
    Image().build(config)
