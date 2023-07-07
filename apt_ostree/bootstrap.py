import os
import subprocess
import sys

from rich.console import Console
from textwrap import dedent

from apt_ostree import constants

class Bootstrap(object):
    def __init__(self, workspace):
        self.console = Console()
        self.workspace_dir = workspace

        self.rootfs = self.workspace_dir.joinpath("rootfs.tar.gz")
        self.components = ["main", "non-free", "contrib"]
        self.cmd = ["mmdebstrap", "--verbose"]

    def mmdebstrap(self, config):
        self.console.print("Running mmdebstrap")

        suite = config.get("suite")
        mirror = config.get("mirror")
        packages = config.get("packages")

        self._check_suite(suite)
        self._get_packages(packages)
        self._get_components()

        self.cmd += [suite, str(self.rootfs), mirror]

        try:
            self.console.print("Running mmdebstrap")
            subprocess.check_call(self.cmd)
        except Exception as ex:
            self.console.print(f"[red]Error[/red]Failed to run mmdebstrap: {ex}")
            raise ex

    def _get_packages(self, packages):
        """Install additional packages"""
        self.console.print("Including addtional packages")
        if packages:
            constants.PACKAGES += packages
        self.cmd += [f"--include={package}"
                    for package in constants.PACKAGES]

    def _get_components(self):
        """Add addtional components"""
        self.console.print("Inclding addtional compoents")
        self.cmd += [f"--component={component}"
                    for component in self.components]
    
    def _check_suite(self, suite):
        """Check for a valid suite that apt-ostree supports"""
        self.console.print("Checking for valid suite")
        if suite not in constants.SUITES:
            self.console.print(f"[red]Error[/red] {suite} is not a valid suite.")
            self.console.print(f"Valid suites are {' '.join(constants.SUITES)}")
            sys.exit(-1)
        self.console.print(f"Found {suite}")

