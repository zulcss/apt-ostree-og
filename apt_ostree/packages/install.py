import apt
import sys

import click
from rich.console import Console
from rich.table import Table

from apt_ostree.utils import eerror

class Install:
    def install(self, packages):
        """apt-get install package"""
        self._apt_cache = self.cache()

        deps = set()
        predeps = set()
        all_deps = set()

        self.packages = self.check_valid_packages(packages)
        if len(self.packages) == 0:
            eerror("No valid packages found...exiting.")
            sys.exit(1)
        else:
            self.show_packages(self.packages, "New packages")
        
        all_deps = self._get_dependencies(deps, predeps, all_deps)
        if len(all_deps) == 0:
            self.console.print("No additional dependencies needed.")
        else:
            self.show_packages(all_deps, "New dependencies")

        if click.confirm("Do you want to continue?"):
            self.deployment_dir = self.ostree.current_deployment()

            self.ostree.mount_rootfs()
            self.ostree.populate_var()

            grid = Table.grid(expand=True)
            grid.add_column()
            grid.add_column(justify="right")

            self.console.print("Installing the following candidates")
            for package in self.packages:
                self.apt_install(package)
                grid.add_row(f"Installed {package} {(self.version(package))}", "[bold magenta]COMPLETED [green]:heavy_check_mark:")
                self.console.print(grid)


            self.ostree.umount_rootfs()
            self.ostree.post_deployment()


        else:
            eerror("Terminating at your request")
            sys.exi(1)

    def _get_dependencies(self, deps, predeps, all_deps):
        """Get all the dependencies for a given package"""
        self.console.print("\nChecking for dependencies")
        for pkg in self.packages:
            deps = self.get_dependencies(
                    self._apt_cache,
                    self.apt_package(pkg),
                    deps,
                    "Depends")
            predeps = self.get_dependencies(
                    self._apt_cache,
                    self.apt_package(pkg),
                    deps,
                    "PreDepends")
        all_deps.update(deps, predeps)
        all_deps = self.check_valid_packages(list(all_deps))
            
        return all_deps
