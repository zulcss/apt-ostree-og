import sys

import click
from rich.table import Table

from apt_ostree.utils import eerror


class Uninstall:
    def uninstall(self, packages):
        """apt-get purge"""
        self._apt_cache = self.cache()

        self.console.print("Removing packages...")

        self.packages = self.check_installed_packages(packages)
        if len(self.packages) == 0:
            eerror("No valid packages found...exiting")
            sys.exit(1)
        else:
            self.show_packages(self.packages, "Installed packages")

        if click.confirm("\nDo you wanto to continue?"):
            self.deployment_dir = self.ostree.current_deployment()

            grid = Table.grid(expand=True)
            grid.add_column()
            grid.add_column(justify="right")

            self.console.print("Uninstalling the following candidates")
            for package in self.packages:
                self.apt_uninstall(package)
                grid.add_row(f"Uninstalled {package} {(self.version(package))}", "[bold magenta]COMPLETED [green]:heavy_check_mark:")
                self.console.print(grid)
            self.ostree.post_deployment()
        else:
            eeror("Terminating at your request")
            sys.exit(1)
