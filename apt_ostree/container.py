"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import shutil

from apt_ostree.bootstrap import Bootstrap
from apt_ostree.build import Build
from apt_ostree.config import Config
from apt_ostree import constants
from apt_ostree.utils import run_command

from rich.console import Console


class Container(object):
    def __init__(self):
        self.console = Console()
        self.config = None

        self.workspace_dir = constants.WORKSPACE.joinpath("build/container")
        self.conf = Config()
        self.bootstrap = Bootstrap(self.workspace_dir)
        self.b = Build(self.workspace_dir)

    def build(self, config):
        """Build the container from a ostree branch"""
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
        self.container_build(self.config["branch"], self.config["repo"],
                             self.config["registry"],
                             self.config["container_name"])

    def container_build(self, branch, repo, registry, name):
        self.console.print("Encapsulating and pusshing to registry")
        url = f"docker://{registry}/{name}"
        run_command(
            ["ostree-ext-cli", "container", "encapsulate", f"--repo={repo}",
             branch, url], cwd=self.workspace_dir)
