import click


def config(f):
    return click.option(
        "-C", "--config",
        help="Config file"
    )(f)
