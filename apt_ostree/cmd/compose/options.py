import click

from apt_ostree import constants


def config(f):
    return click.option(
        "-C", "--config",
        help="Config file"
    )(f)

def packages(f):
    return click.option(
        "-P", "--packages",
        help="Extra packages to install",
    )(f)


def arch(f):
    return click.option(
        "--arch",
        default="amd64",
        help="Architecture to use"
    )(f)
