"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import click


def config(f):
    return click.option(
        "-C", "--config",
        help="Config file"
    )(f)
