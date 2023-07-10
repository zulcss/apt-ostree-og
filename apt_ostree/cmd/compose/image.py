import click

from apt_ostree.cmd.compose import options
from apt_ostree.image import Image


@click.command(help="Compose an image")
@click.pass_context
@options.config
def image(ctxt, config):
    Image().build(config)
