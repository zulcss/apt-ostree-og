from time import sleep
import shutil
import subprocess
import sys

from rich.console import Console

from apt_ostree.bootstrap import Bootstrap
from apt_ostree import constants
from apt_ostree.config import Config
from apt_ostree.ostree import ostree

class Image(object):
    def __init__(self):
        self.console = Console()
        self.config = None

        self.workspace_dir = constants.WORKSPACE.joinpath("build/image")
        self.conf = Config()
        self.bootstrap = Bootstrap(self.workspace_dir)
    
    def build(self, config):
        """Build an image."""
        self.console.print("Copying configuration to workspace")
        if self.workspace_dir.exists():
            shutil.rmtree(self.workspace_dir)
        shutil.copytree(config, self.workspace_dir)

        self.config = self.conf.load_config(config)
        self.bootstrap.mmdebstrap(self.config)

        self._create_repo(self.config["repo"])
        self._create_ostree_commit(
                self.config["branch"],
                self.config["repo"],
                self.config["suite"],
                self.config["ostree_template"]
        )
        self._create_image(
                self.config["branch"],
                self.config["repo"],
                self.config["name"],
                self.config["size"],
                self.config["suite"],
                self.config["image_template"]
        )

    def _create_repo(self, repo):
        """Create the initial ostree repository"""
        self.console.print("Creating ostree repository.")
        ostree("init", 
               repo=str(self.workspace_dir.joinpath(repo)), mode="archive")

    def _create_ostree_commit(self, branch, repo, suite, template):
        """Create an ostree branch via a rootfs tarball"""
        self.console.print("Commiting rootfs to ostree")
        subprocess.check_call(["debos",
                              "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", "architecture:amd64",
                               "-t", f"suite:{suite}",
                               template], cwd=self.workspace_dir)
    
    def _create_image(self, branch, repo, image, size, suite, template):
        """Create a raw image bootable via qemu"""
        self.console.print("Createing ostree image")
        subprocess.check_call(["debos",
                               "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", f"image:{image}",
                               "-t", f"size:{size}",
                               "-t", "architecture:amd64",
                               "-t", f"suite:{suite}",
                               template], cwd=self.workspace_dir)
