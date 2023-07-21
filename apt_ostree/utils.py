"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

from rich.console import Console

import subprocess

console = Console()

def eerror(msg):
    console.print(f"[red]Error [/red]" + msg)

def run_sandbox_command(args, rootfs, env=None):
    try:
        cmd = [
            "bwrap",
            "--die-with-parent",
            "--bind", str(rootfs), "/",
            "--dir", "/tmp",
            "--dir", "/run",
            "--dev", "/dev",
            "--proc", "/proc",
            "--ro-bind", "/sys", "/sys",
            "--symlink", f"{rootfs}/usr/etc", "/etc",
            "--share-net",
            "--unshare-pid",
            "--unshare-uts",
            "--unshare-ipc",
            "--unshare-cgroup-try",
        ]
        cmd += args
        print(cmd)
        subprocess.run(
            cmd,
            env=env,
            check=False)
    except subprocess.CalledProcessError as error:
        console.print(error)


def run_command(cmd, cwd=None):
    try:
        return subprocess.run(
            cmd,
            encoding="utf8",
            cwd=cwd,
            check=True)
    except subprocess.CalledProcessError as error:
        console.print(error)
