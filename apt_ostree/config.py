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
            "suite": cfg.get("suite", "bookwork")
            "rootfs": self.workspace_dir.joinpath("rootfs.tar.gz")
        }
