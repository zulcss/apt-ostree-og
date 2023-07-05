import os
import shutil
import subprocess
import sys

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
        subprocess.run(
                ["ostree", "checkout", csum, self.deployment_dir],
                check=True)
        shutil.move(
            self.deployment_dir.joinpath("usr/etc"),
            self.deployment_dir.joinpath("etc"))
        subprocess.run(
            ["systemd-tmpfiles", "--create", "--root", self.deployment_dir],
            check=True)
        return self.deployment_dir
        
    def post_deployment(self):
        shutil.move(
            self.deployment_dir.joinpath("etc"),
            self.deployment_dir.joinpath("usr/etc"))
        shutil.rmtree(
            self.deployment_dir.joinpath("var"))
        os.mkdir(os.path.join (self.deployment_dir, "var"), 0o755)

        branch = f"debian/bookworm-test"
        subprocess.run(
            ["ostree", "commit", f"--branch={branch}", str(self.deployment_dir)],
            check=True)
        subprocess.run(
            ["ostree", "admin", "deploy", branch, "--retain-rollback", "--karg-proc-cmdline"],
            check=True)
        subprocess.run(
            ["update-grub"], check=True
        )
 
