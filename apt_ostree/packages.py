import sys

import apt

from rich.console import Console

from apt_ostree.constants import WORKSPACE
from apt_ostree.ostree import Ostree

class Packages(object):
    def __init__(self):
        self.workspace = WORKSPACE
        self.deployment_dir = self.workspace.joinpath("deployments")
        self.packages = []
        self._apt_cache = None
        self.console = Console()
        self.ostree = None

    def _cache(self):
        if not self._apt_cache:
            try:
                self.console.print("Running apt-get update")
                self._apt_cache = apt.Cache()
                self._apt_cache.update()
            except AttributeError as e:
                self.console.print(f"[red]Failed to load apt cache[/red]: {e}")
                sys.exit(-1)
        return self._apt_cache

    def install(self, packages):
        """Install package"""
        self._apt_cache = self._cache()

        self.packages = self.get_packages(packages)
        if len(self.packages) == 0:
            self.console.print("No valid packages found...exiting")
            sys.exit(-1)

        self.ostree = Ostree(self.deployment_dir)
        self.deployment_dir = self.ostree.deployment()

        self.console.print("Going to install the following packages")
        for package in self.packages:
            ver = self.get_version(package)
            self.console.print(f"{package} {ver}")

    def get_version(self, package):
        return self._apt_cache[package].candidate.version

    def get_packages(self, packages):
        pkgs = []
        for package in packages:
            if package in self._apt_cache:
                pkg = self._apt_cache[package]
                if not pkg.is_installed:
                    pkgs.append(package)
        return pkgs

