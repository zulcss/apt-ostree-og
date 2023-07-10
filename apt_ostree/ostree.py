from datetime import datetime
import os
import shutil
import pathlib
import subprocess
import sys

from apt_ostree.utils import run_sandbox_command
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
    def __init__(self, deployment_dir):
        self.console = Console()
        self.deployment_dir = deployment_dir
        self.rootdir = pathlib.Path("/")

    def deployment(self):
        sysroot = OSTree.Sysroot()
        sysroot.load()

        deployments = sysroot.get_deployments()
        if len(deployments) == 0:
            self.console.print("[red]Unable to determine deployment[/red]")
            sys.exit(1)

        csum = deployments[0].get_csum()
        self.console.print(f"Checking out {csum[:10]} to {self.deployment_dir}")
        self.deployment_dir = self.deployment_dir.joinpath(csum)
        if self.deployment_dir.exists():
            shutil.rmtree(self.deployment_dir)

        run_command(
                ["ostree", "checkout", csum, self.deployment_dir])
        shutil.move(
            self.deployment_dir.joinpath("usr/etc"),
            self.deployment_dir.joinpath("etc"))
        self.populate_var()
        return self.deployment_dir

    def populate_var(self):
        tmpdir = self.deployment_dir.joinpath("var")
        ret = run_command(
               ["systemd-tmpfiles", "--create", f"--root={self.deployment_dir}"])
        if ret.returncode not in [0, 65]:
           self.console.print(f"Failed to create {target}")

        self.deployment_dir.joinpath("var/cache/apt/partial").mkdir(
             parents=True, exist_ok=True)
        run_sandbox_command(
             ["touch", "/var/lib/dpkg/lock-frontend"], self.deployment_dir)
        run_sandbox_command(["apt-get", "update"], self.deployment_dir)
        run_sandbox_command(["apt-get", "install", "-y", "locales"], self.deployment_dir)
        
    def post_deployment(self):
        shutil.move(
            self.deployment_dir.joinpath("etc"),
            self.deployment_dir.joinpath("usr/etc"))
        shutil.rmtree(
            self.deployment_dir.joinpath("var"))
        os.mkdir(os.path.join (self.deployment_dir, "var"), 0o755)

        now = datetime.now()
        now = now.strftime("%Y%m%d%H%M%S")
        branch = f"debian/bookworm-local/{now}"

        self.console.print(f"Committing new branch to {branch}")
        run_command(
            ["ostree", "commit", f"--branch={branch}", str(self.deployment_dir)])
        self.console.print(f"Deploying {branch}")
        run_command(
            ["ostree", "admin", "deploy", branch, "--retain-rollback", "--karg-proc-cmdline"])
        self.console.print(f"Updating grub")
        run_command(["update-grub"])

        self.console.print("Saving state information")
 
