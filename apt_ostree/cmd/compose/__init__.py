import click

from . import container
from . import deployment
from . import image


@click.group(help="Commands to build a container/image")
@click.pass_context
def compose(ctxt):
    pass


compose.add_command(image.image)
compose.add_command(deployment.deployment)
compose.add_command(container.container)
