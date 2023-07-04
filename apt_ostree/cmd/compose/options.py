import click

from apt_ostree import constants


def branch(f):
    return click.option(
        "-b", "--branch",
        help="ostree repo branch to create"
    )(f)


def repo(f):
    return click.option(
        "-r", "--repo",
        default="ostree_repo",
        help="ostree repo to create"
    )(f)


def packages(f):
    return click.option(
        "-P", "--packages",
        help="Extra packages to install",
    )(f)


def suite(f):
    return click.option(
        "--suite",
        default="bookworm",
        help="Debian version to bootstrap"
    )(f)


def mirror(f):
    return click.option(
        "--mirror",
        default="http://deb.debian.org/debian",
        help="Debian mirror to use"
    )(f)


def arch(f):
    return click.option(
        "--arch",
        default="amd64",
        help="Architecture to use"
    )(f)
