import os
import sys

from rich.console import Console

from apt_ostree import constants
from apt_ostree.log import log_step

import subprocess

console = Console()


def run_cmd(cmd, verbose=False):
    log_step(f"Running: {cmd}")
    if verbose:
        return subprocess.check_call(cmd.split())
    else:
        return subprocess.run(cmd.split(), check=True)

def checkroot():
    if os.geteuid() != 0:
        eerror("Superuser privileges required.")
        sys.exit(-1)

def is_ostree():
    """Detect if ostree is deployed"""
    if not constants.OSTREE_PATH.exists():
        console.print("[red]error[/red] /ostree not found, exiting")
        sys.exit(-1)


def ostree(*args, _input=None, **kwargs):
    """Run the osteee command"""
    args = list(args) + [f'--{k}={v}' for k, v in kwargs.items()]
    subprocess.run(["ostree"] + args,
                   encoding="utf8",
                   stdout=sys.stderr,
                   input=_input,
                   check=True)
def eerror(msg):
    """Print an error message"""
    console = Console(stderr=True, style="bold red")
    console.print("{}".format(msg))

def einfo(msg):
    console.print("{}".format(msg))
