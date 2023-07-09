import os
import sys

from rich.console import Console

import subprocess

console = Console()

def run_sandbox_command(args, rootfs):
    try:
        cmd = [
            "bwrap",
            "--die-with-parent",
            "--bind", rootfs, "/",
            "--dev", "/dev",
            "--proc", "/proc",
            "--ro-bind", "/sys", "/sys"]
        cmd += args
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            encoding="utf8",
            check=False)
    except subprocess.CalledProcessError as error:
        console.print(error)

def run_command(cmd):
    try:
        return subprocess.run(
            cmd,
             stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            encoding="utf8",
            check=False)
    except subprocess.CalledProcessError as error:
        console.print(error)


        
