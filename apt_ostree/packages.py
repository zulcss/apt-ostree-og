import sys
import subprocess
import apt

import click
from rich.console import Console
from rich.table import Table

from apt_ostree.constants import WORKSPACE
from apt_ostree.ostree import Ostree
from apt_ostree.ostree import ostree
from apt_ostree.utils import run_sandbox_command

verbosity = 0

class Packages(object):
    def __init__(self):
        self.workspace = WORKSPACE
        self.deployment_dir = self.workspace.joinpath("deployments")
        self.packages = []
        self._apt_cache = None
        self.console = Console()
        self.ostree = None

        self.deployment_dir.mkdir(parents=True, exist_ok=True)

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

    def _apt_package(self, package):
        try:
            return self._cache()[package]
        except KeyError:
            self.console.print("Unable to find package")

    def install(self, packages):
        """Install package"""
        print(verbosity)
        self._apt_cache = self._cache()
        deps = set()
        predeps = set()
        all_deps = set()

        self.packages = self.get_packages(packages)
        if len(self.packages) == 0:
            self.console.print("No valid packages found...exiting")
            sys.exit(-1)

        self.show_packages()
        self.show_dependencies(all_deps, deps, predeps)

        if click.confirm("Do you want to continue?"):
            self.ostree = Ostree(self.deployment_dir)
            self.deployment_dir = self.ostree.deployment()

            self.apt_update()
            self.console.print("Installing the following package candidates")
            for package in self.packages:
                ver = self.get_version(package)
                self.console.print(f"Installing {package} ({ver})")
                self.apt_install(package)

            self.ostree.post_deployment()
        else:
            self.console.print("Terminating...")
            sys.exit(1)


    def show_dependencies(self, all_deps, deps, predeps): 
        for pkg in self.packages:
            deps = self.get_dependencies(
                self._apt_cache,
                self._apt_package(pkg),
                deps,
               "Depends")
            predeps = self.get_dependencies(
                self._apt_cache,
                self._apt_package(pkg),
                deps,
               "PreDepends")
        all_deps.update(deps, predeps)
        all_deps = sorted(all_deps)

        table = Table(title="New Dependencies", expand=True, box=None)
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Architecture")
        table.add_column("Component")
        table.add_column("Origin")
        table.add_column("Size")
        for pkg in all_deps:
            d = self._apt_package(pkg)
            if not d.installed:
                table.add_row(d.name,
                              d.candidate.version,
                              str(d.candidate.architecture),
                              str(d.candidate.origins[0].archive),
                              str(d.candidate.origins[0].origin),
                              str(d.candidate.size))

        self.console.print(table)

         
    def get_dependencies(self, cache, pkg, deps, key="Depends"):
        candver = cache._depcache.get_candidate_ver(pkg._pkg)
        if candver is None:
            return deps
        dependslist = candver.depends_list
        if key in dependslist:
            for depVerList in dependslist[key]:
                for dep in depVerList:
                    if dep.target_pkg.name in cache:
                        if (
                            pkg.name != dep.target_pkg.name
                            and dep.target_pkg.name not in deps
                        ):
                            deps.add(dep.target_pkg.name)
                            self.get_dependencies(cache, cache[dep.target_pkg.name], deps, key)
        return deps

    def show_packages(self):
        table = Table(title="New Packages",expand=True, box=None)
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Architecture")
        table.add_column("Component")
        table.add_column("Origin")
        table.add_column("Size")
        for package in self.packages:
            table.add_row(package, 
                          self._apt_package(package).candidate.version,
                          str(self._apt_package(package).candidate.architecture),
                          str(self._apt_package(package).candidate.origins[0].archive),
                          str(self._apt_package(package).candidate.origins[0].origin),
                          str(self._apt_package(package).candidate.size))
        self.console.print(table)

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

    def apt_update(self):
        self.console.print("Running apt-get update")
        run_sandbox_command(["apt-get", "update"], self.deployment_dir)

    def apt_install(self, package):
        env = dict(
            DEBIAN_FRONTEND="noninteractive",
            DEBCONF_INTERACTIVE_SEEN="true",
            KERNEL_INSTALL_BYPASS="1",
            INITRD="No",
        )

        run_sandbox_command(["apt-get", "install", "-y", package], self.deployment_dir, env=env)
