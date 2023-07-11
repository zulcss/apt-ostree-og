"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import subprocess

from rich.console import Console

from apt_ostree.ostree import ostree


class Build(object):
    def __init__(self, workspace):
        self.console = Console()
        self.workspace_dir = workspace

    def create_repo(self, repo):
        """Create the initial ostree repository"""
        self.console.print("Creating ostree repository.")
        ostree("init",
               repo=str(self.workspace_dir.joinpath(repo)), mode="archive")

    def create_ostree_commit(self, branch, repo, suite, template):
        """Create an ostree branch via a rootfs tarball"""
        self.console.print("Commiting rootfs to ostree")
        subprocess.check_call(["debos",
                               "-c", "4",
                               "-m", "16G",
                              "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", "architecture:amd64",
                               "-t", f"suite:{suite}",
                               template], cwd=self.workspace_dir)

    def create_image(self, branch, repo, image, size, suite, template):
        """Create a raw image bootable via qemu"""
        self.console.print("Createing ostree image")
        subprocess.check_call(["debos",
                               "-v",
                               "-c", "4",
                               "-m", "16G",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", f"image:{image}",
                               "-t", f"size:{size}",
                               "-t", "architecture:amd64",
                               "-t", f"suite:{suite}",
                               template], cwd=self.workspace_dir)
