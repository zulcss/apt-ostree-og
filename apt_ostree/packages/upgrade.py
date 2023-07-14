import apt_pkg
import sys

from rich.table import Table

class Upgrade:
    def upgrade(self):
        """"apt-get upgrade"""
        self.deployment_dir = self.ostree.current_deployment()

        self.console.print("Upgrading packages")
        self.apt_upgrade()

        self.ostree.post_deployment()

    def show_upgrades(self):
        apt_pkg.init()
        cache = apt_pkg.Cache()

        depcache.init()
        if depcache.broken_count > 0:
            self.console.print("[red]Error [/red] Broken packages exists")
            sys.exit(1)

        # simulate an upgrade but dont actually do the upgrade
        try:
            depcache.upgrade(True)
            if depcache.del_count > 0:
                depcache.init()
            debpcache.upgrade()
        except SystemError as ex:
            self.console.print(f"[red]Error: [/red] Couldn't mark the upgrade {e}")
            sys.exit(0)

        table = Table(title="Packages that need updating", expand=True, box=None)
        table.add_column("Name")
        table.add_column("Current Version")
        table.add_column("New Version")
        for pkg in cache.packages:
            candidate = depcache.get_candidate_ver(pkg)
            if depcache.marked_upgrade(pkg):
                table.add_row(
                    pkg.name,
                    pkg.current_ver.ver_str,
                    candidate.ver_str)
        self.console.print(table)
