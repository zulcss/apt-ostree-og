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

def branch(f):
    return click.option(
        "-b", "--branch",
        help="Ostree deployment"
    )(f)

def repo(f):
    return click.option(
        "-r", "--repo",
        default="/var/repository/debian",
        help="Path to package repo"
    )(f)

def suite(f):
    return click.option(
        "-s", "--suite",
        help="suite to drop package into",
        default="bookworm"
    )(f) 

