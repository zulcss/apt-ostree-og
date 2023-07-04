import click

from apt_ostree import constants


def config(f):
    return click.option(
        "-C", "--config",
        help="Config file"
    )(f)
