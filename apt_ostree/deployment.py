import shutil
import subprocess
import sys

from rich.console import Console

from apt_ostree.build import Build
from apt_ostree.bootstrap import Bootstrap
from apt_ostree import constants
from apt_ostree.config import Config
from apt_ostree.ostree import ostree

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
