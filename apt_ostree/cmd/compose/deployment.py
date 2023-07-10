import click

from apt_ostree.cmd.compose import options
from apt_ostree.deployment import Deployment


@click.command(help="Compose a demployment")
@click.pass_context
@options.config
def deployment(ctxt, config):
    Deployment().build(config)
