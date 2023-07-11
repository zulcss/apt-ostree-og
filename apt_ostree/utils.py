"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

from rich.console import Console

import subprocess

console = Console()


def run_sandbox_command(args, rootfs, verbose=True, env=None):
    stdin = None
    stdout = subprocess.DEVNULL,
    stderr = subprocess.STDOUT,

    if verbose:
        stdout = None
        stderr = None

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
            stdout=stdout,
            stdin=stdin,
            stderr=stderr,
            encoding="utf8",
            env=env,
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
