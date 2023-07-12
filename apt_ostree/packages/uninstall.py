import apt
import sys

import click
from rich.console import Console
from rich.table import Table

from apt_ostree.constants import WORKSPACE
from apt_ostree.ostree import Ostree
from apt_ostree.utils import run_sandbox_command

class Uninstall(object):
    def __init__(self):
        self.workspace = WORKSPACE
        self.deployment_dir = self.workspace.joinpath("deployments")
        self.packages = []
        self._apt_cache = None
        self.console = Console()
        self.ostree = None

        self.deployment_dir.mkdir(parents=True, exist_ok=True)

    def _cache(self):
        """Setup the apt-cache"""
        if not self._apt_cache:
            try:
                self.console.print("Running apt-get update")
                self._apt_cache = apt.Cache()
                self._apt_cache.update()
            except AttributeError as e:
                self.console.print(f"[red]Failed to load apt cache[/red]: {e}")
                sys.exit(-1)
        return self._apt_cache

    def _apt_package(self, package):
        """Query the apt-cahce for a given pckage"""
        try:
            return self._cache()[package]
        except KeyError:
            self.console.print("Unable to find package")

    def _get_packages(self, packages):
         """Check the packages exist and arei ntalled"""
         pkgs = []
         for package in packages:
            if package in self._apt_cache:
                pkg = self._apt_cache[package]
                if pkg.is_installed:
                    pkgs.append(package)
                else:
                    self.console.print(f"{package} is not installed...skipping")
         return pkgs

    def run(self, packages):
        self._apt_cache = self._cache()

        self.packages = self._get_packages(packages)
        if len(self.packages) == 0:
            self.console.print("No packages to uninstall...exiting")
            sys.exit(1)
        
        self.console.print("Going to remove the following packages:\n")

        self.show_packages()

        if click.confirm("Do you want to continue?"):
            self.ostree = Ostree(self.deployment_dir)
            self.deployment_dir = self.ostree.deployment()

            for package in self.packages:
                self.console.print(f"Uninstalling {package}")
                self.apt_uninstall(package)

            self.ostree.post_deployment()
        else:
            self.console.print("Terminating...")
            sys.exit(1)

    def show_packages(self):
        table = Table(expand=True, box=None)
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Architecture")
        table.add_column("Component")
        table.add_column("Origin")
        table.add_column("Size")
        for package in self.packages:
            table.add_row(package,
                          self._apt_package(
                              package).candidate.version,
                          str(self._apt_package(
                              package).candidate.architecture),
                          str(self._apt_package(
                              package).candidate.origins[0].archive),
                          str(self._apt_package(
                              package).candidate.origins[0].origin),
                          str(self._apt_package(package).candidate.size))
        table.add_row()

        self.console.print(table)

    def apt_uninstall(self, package):
        env = dict(
            DEBIAN_FRONTEND="noninteractive",
            DEBCONF_INTERACTIVE_SEEN="true",
            KERNEL_INSTALL_BYPASS="1",
            INITRD="No",
        )
        run_sandbox_command(
            ["apt-get", "purge", "-y", package],
            self.deployment_dir, env=env)
