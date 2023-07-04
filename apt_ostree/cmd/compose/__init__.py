import click

from . import image


@click.group(help="Compands to build a container/image")
@click.pass_context
def compose(ctxt):
    pass


compose.add_command(image.image)
