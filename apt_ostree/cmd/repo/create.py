import click


@click.command(help="Create repo configuration")
@click.pass_context
@click.option(
        "-R", "--repo",
        help="Path to apt repo")
@click.option(
        "-S", "--suite",
        help="Suite to create")
@click.option(
        "-P", "--pocket",
        help="pocket to create")
def create(ctxt):
    pass
