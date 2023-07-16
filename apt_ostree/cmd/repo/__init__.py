import click

from . import create

@click.group(help="commands to create an apt repository")
@click.pass_context
def repo(ctxt):
    pass

