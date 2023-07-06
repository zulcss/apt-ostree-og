import click

from apt_ostree.deployment import Deployment
from apt_ostree.cmd.compose import options

@click.command(help="Compose a demployment")
@click.pass_context
@options.config
def deployment(ctxt, config):
    Deploymente().build(config)
