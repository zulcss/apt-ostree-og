import sys

from rich.console import Console
import yaml

class Config(object):
    def __init__(self):
        self.console = Console()

    def load_config(self, config):
        cfg = {}
        try:
            with open(config, "r") as f:
                cfg = yaml.safe_load(f)
        except IOError:
            pass

        rootfs = cfg.get("rootfs", None)
        if rootfs is None:
            self.console.print("[red]Unable to parse rootfs config, using defaults.[/red]")
        ostree = cfg.get("ostree", None)
        if ostree is None:
            self.console.print("[red]Unable to parse ostree config, using defaults.[/red]")

        return {
            "suite": rootfs.get("suite", "bookwork"),
            "branch": ostree.get("branch", "debian/bookworm"),
            "repo": ostree.get("repo", "ostree_repo"),
        }
