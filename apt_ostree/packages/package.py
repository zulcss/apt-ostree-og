from rich.console import Console

from apt_ostree.constants import WORKSPACE
from apt_ostree.ostree import Ostree
from apt_ostree.packages.install import Install
from apt_ostree.packages.uninstall import Uninstall
from apt_ostree.packages.upgrade import Upgrade
from apt_ostree.packages.apt import APT

class Package(Install, Uninstall, Upgrade, APT):
    def __init__(self):
        self.console = Console()
        self.workspace = WORKSPACE
        self.deployment_dir = self.workspace.joinpath("deployments")
        self.packages = []
        self._apt_cache = None
        self.ostree = Ostree()

        self.env = dict(
            DEBIAN_FRONTEND="noninteractive",
            DEBCONF_INTERACTIVE_SEEN="true",
            KERNEL_INSTALL_BYPASS="1",
            INITRD="No",
        )

    def package_list(self):
        self.console.print("package list")
        self.apt_list()

    def package_install(self, packages):
        self.install(packages)

    def package_uninstall(self, packages):
        self.uninstall(packages)

    def package_upgrade(self):
        self.upgrade()
