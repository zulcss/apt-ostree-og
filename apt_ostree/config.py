import pathlib
import sys

from rich.console import Console
import yaml

class Config(object):
    def __init__(self):
        self.console = Console()

    def load_config(self, config):
        cfg = {}
        try:
            config = pathlib.Path(config)
            config = config.joinpath("config.yaml")

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
        image = cfg.get("image", None)
        if image is None:
            self.console.print("[red]Unable to parse image config, using defaults.[/red]")
        container = cfg.get("container", None)
        if container is None:
            self.console.print("[red]Unable to parse container config, using defaults.[/red]")

        return {
            "suite": rootfs.get("suite", "bookwork"),
            "mirror": rootfs.get("mirror", "http://deb.deian.org/debian"),
            "packages": rootfs.get("packages", []),
            "branch": ostree.get("branch", "debian/bookworm"),
            "repo": ostree.get("repo", "ostree_repo"),
            "ostree_template": ostree.get("template", "debian-ostree-commit.yaml"),
            "name": image.get("name", "debian-ostree-qemu-uefi-amd64.img"),
            "size": image.get("size", "20G"),
            "image_template": image.get("template", "debian-ostree-amd64.yaml"),
            "container_name": container.get("container_name", f"debian-ostree-dev:latest"),
            "registry": container.get("registry", "quay.io"),
        
        }
