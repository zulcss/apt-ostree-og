"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import datetime
import os
import shutil

from rich.console import Console

from apt_ostree.bootstrap import Bootstrap
from apt_ostree.build import Build
from apt_ostree.config import Config
from apt_ostree.system import get_local_ip
from apt_ostree import utils
from apt_ostree import constants


class Deployment(object):
    def __init__(self):
        self.console = Console()
        self.config = None

        self.workspace_dir = constants.WORKSPACE.joinpath("build/repo")
        self.conf = Config()
        self.bootstrap = Bootstrap(self.workspace_dir)
        self.b = Build(self.workspace_dir)

    def build(self, config):
        """Build an image."""
        self.console.print("Copying configuration to workspace")
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
        shutil.copytree(config, self.workspace_dir)

        self.config = self.conf.load_config(config)
        self.bootstrap.mmdebstrap(self.config)

        self.b.create_repo(self.config["repo"])
        self.b.create_ostree_commit(
            self.config["branch"],
            self.config["repo"],
            self.config["suite"],
            self.config["ostree_template"]
        )
    
    def populate_var(self):
        host = self.deployment_dir.joinpath("usr/etc/hosts")
        with open(host, "a") as outfile:
            ipaddress = get_local_ip()
            outfile.write(f"{ipaddress}\tarchive\n")
        utils.run_sandbox_command(
            ["systemd-tmpfiles", "--create", "--remove", "--boot",
             "--prefix=/var", "--prefix=/run"], self.deployment_dir)
        self.deployment_dir.joinpath("var/cache/apt/partial").mkdir(
            parents=True, exist_ok=True)
        utils.run_sandbox_command(
            ["touch", "/var/lib/dpkg/lock-frontend"], self.deployment_dir)
        utils.run_sandbox_command(["apt-get", "update"], self.deployment_dir)
        utils.run_sandbox_command(["apt-get", "install", "-y",
                            "locales"], self.deployment_dir)

    def post_deployment(self):
        shutil.rmtree(
            self.deployment_dir.joinpath("etc"))
        shutil.rmtree(
            self.deployment_dir.joinpath("var"))
        os.mkdir(os.path.join(self.deployment_dir, "var"), 0o755)

        now = datetime.now()
        now = now.strftime("%Y%m%d%H%M%S")
        branch = f"debian/bookworm-local/{now}"

        self.console.print(f"Committing new branch to {branch}")
        utils.run_command(
            ["ostree", "commit", f"--branch={branch}",
             str(self.deployment_dir)])
        self.console.print(f"Deploying {branch}")
        utils.run_command(
            ["ostree", "admin", "deploy", branch, "--retain-rollback",
             "--karg-proc-cmdline"])
        self.console.print(f"Updating grub")
        utils.run_command(["update-grub"])

