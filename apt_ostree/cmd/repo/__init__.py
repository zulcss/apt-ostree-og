import click

from . import add
from . import create
from apt_ostree.cmd.repo.list import list_packages
from apt_ostree.system import check_user

@click.group(help="Commands to manage debian repository")
@click.pass_context
def repo(ctxt):
    check_user()

repo.add_command(create.create)
repo.add_command(add.add)
repo.add_command(list_packages)
