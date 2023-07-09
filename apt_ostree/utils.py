import os
import sys

from rich.console import Console

from apt_ostree import constants
from apt_ostree.log import log_step

import subprocess

console = Console()

def run_command(args, rootfs):
    cmd = [
     "bwrap",
     "--die-with-parent",
     "--bind", rootfs, "/",
     "--dev", "/dev",
     "--proc", "/proc",
     "--ro-bind", "/sys", "/sys"]
    cmd += args
    subprocess.run(cmd, check=True)

        
