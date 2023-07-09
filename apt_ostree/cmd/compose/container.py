import click

from apt_ostree.container import Container
from apt_ostree.cmd.compose import options

@click.command(help="Compose an image")
@click.pass_context
@options.config
def container(ctxt, config):
    Container().build(config)
