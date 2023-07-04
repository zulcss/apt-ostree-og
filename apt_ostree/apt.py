import apt
import subprocess
from rich.console import Console

class Apt(object):
    def __init__(self):
        self.console = Console()
        self._apt_cache = None

    def _cache(self):
        if not self._apt_cache:
            try:
                self._apt_cache = apt.Cache()
                self._apt_cache.update()
            except AttributeError as e:
                self.console.print(f"[red]Failed to load apt cache[/red]: {e}")
                sys.exit(-1)
        return self._apt_cache

    def get_package(self, package):
        try:
            return self._cache()[package]
        except KeyError:
            self.console.print(f"[red]{package}[/red] does not exist.")


    def _bwrap(self, c, rootfs):
        cmd = [
            "bwrap",
            "--die-with-parent",
            "--bind", rootfs, "/",
            "--dev", "/dev",
            "--proc", "/proc",
             "--ro-bind", "/sys", "/sys",
             *c]
        subprocess.run(cmd)


    def apt_update(self, rootfs):
        self._bwrap(["apt-get", "update", "-y"], rootfs)

    def apt_install(self, rootfs, package):
        self._bwrap(["apt-get", "install", "--no-install-recommends", "-y", package], rootfs)

