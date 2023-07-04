import click

from . import compose
from . import install

@click.group(
    help=f"\nHyrbid images/packages management system."
)
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)

cli.add_command(install.install)
cli.add_command(compose.compose)

def main():
    cli(prog_name="apt-ostree")
