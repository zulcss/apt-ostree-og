import apt

from rich.table import Table

from apt_ostree.utils import eerror
from apt_ostree.utils import run_sandbox_command

class APT:
    """ apt operations """
    def cache(self):
        """Update the local packaeg cache"""
        if not self._apt_cache:
            try:
                self.console.print("Updating local package cache")
                self._apt_cache = apt.Cache()
                self._apt_cache.update()
            except  AttributeError as e:
                eerror(f"Failed to load apt cache: {e}")
                sys.exit(-1)
        return self._apt_cache

    def apt_package(self, package):
        """Query the apt cache for a given package"""
        try:
            return self.cache()[package]
        except KeyError:
            eerror(f"Unable to find {package}")
    
    def check_valid_packages(self, packages):
        """Check for existing non-installed package"""
        pkgs = []
        for package in packages:
            if package in self._apt_cache:
                pkg = self.apt_package(package)
                if not pkg.is_installed:
                    pkgs.append(package)
        return pkgs

    def check_installed_packages(self, packages):
        pkgs = []
        for package in packages:
            if package in self._apt_cache:
                pkg = self.apt_package(package)
                if pkg.is_installed:
                    pkgs.append(package)
        return pkgs

    def get_dependencies(self, cache, pkg, deps, key="Depends"):
        """Recursively collect the dependencies for a given package"""
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
                            self.get_dependencies(
                                cache, cache[dep.target_pkg.name], deps, key)
        return deps

    def show_packages(self, packages, t):
        """Display a table of package information"""
        table = Table(title=t, expand=True, box=None)
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Architecture")
        table.add_column("Component")
        table.add_column("Origin")
        table.add_column("Size")
        for package in packages:
             table.add_row(package,
                          self.apt_package(
                              package).candidate.version,
                          str(self.apt_package(
                              package).candidate.architecture),
                          str(self.apt_package(
                              package).candidate.origins[0].archive),
                          str(self.apt_package(
                              package).candidate.origins[0].origin),
                          str(self.apt_package(package).candidate.size))


        self.console.print(table), 

    def version(self, package):
        """Query the apt cache for package version"""
        return self.apt_package(package).candidate.version
            
    def apt_install(self, package):
        """Run apt-get install"""
        run_sandbox_command(["apt-get", "install", "-y", package],
                            self.deployment_dir, env=self.env)
    
    def apt_uninstall(self, package):
        """Run apt-get purge"""
        run_sandbox_command(["apt-get", "purge", "-y", package],
                            self.deployment_dir, env=self.env)

    def apt_upgrade(self):
        """Run apt-get upgrade"""
        run_sandbox_command(["apt-get", "upgrade", "-y"],
                            self.deployment_dir, env=self.env)

