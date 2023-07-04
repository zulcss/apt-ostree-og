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
            self.console.print("Unable to parse configuration file, using defaults.")

        return {
            "suite": cfg.get("suite", "bookwork"),
            "branch": cfg.get("branch", "debian/bookworm"),
            "repo": cfg.get("repo", "ostree_repo"),
        }
