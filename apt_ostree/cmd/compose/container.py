import click

from apt_ostree.cmd.compose import options
from apt_ostree.container import Container


@click.command(help="Compose an image")
@click.pass_context
@options.config
def container(ctxt, config):
    Container().build(config)
