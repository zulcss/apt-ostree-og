"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

from datetime import datetime
import os
import pathlib
import shutil
import subprocess
import sys

from apt_ostree import constants
from apt_ostree.deployment import Deployment
from apt_ostree.utils import run_command
from rich.console import Console

import gi
gi.require_version('OSTree', '1.0')
from gi.repository import OSTree


def ostree(*args, _input=None, **kwargs):
    """Wrapper for ostree"""
    args = list(args) + [f'--{k}={v}' for k, v in kwargs.items()]
    print("ostree " + " ".join(args), file=sys.stderr)
    subprocess.run(["ostree"] + args,
                   encoding="utf8",
                   stdout=sys.stderr,
                   input=_input,
                   check=True)


class Ostree(object):
    def __init__(self):
        self.console = Console()
        self.deployment = Deployment()
        self.workspace_dir = constants.WORKSPACE
        self.deployment_dir = self.workspace_dir.joinpath("deployments")

        self.deployment_dir.mkdir(parents=True, exist_ok=True)

    def current_deployment(self):
        """Deploy the current deployment to a temporary directory"""
        sysroot = OSTree.Sysroot()
        sysroot.load()

        deployments = sysroot.get_deployments()
        if len(deployments) == 0:
            self.console.print("[red]Unable to determine deployment[/red]")
            sys.exit(1)

        csum = deployments[0].get_csum()
        self.console.print(
            f"Checking out {csum[:10]} to {self.deployment_dir}")
        self.deployment_dir = self.deployment_dir.joinpath(csum)
        if self.deployment_dir.exists():
            shutil.rmtree(self.deployment_dir)

        run_command(
            ["ostree", "checkout", csum, self.deployment_dir])
        self.deployment.populate_var()
        return self.deployment_dir