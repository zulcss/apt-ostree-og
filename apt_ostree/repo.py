import subprocess
import shutil
import sys
import pathlib
import textwrap


from rich.console import Console
from rich.table import Table

class Repo(object):
    def __init__(self, repo_dir):
        self.repo_dir = pathlib.Path(repo_dir)
        self.console = Console()

    def create_repo(self, distro, pocket):
        """Create repo used for reprepo"""  

        # Verify the debian repo doesnt exist.
        if not self.repo_dir.exists():
            self.repo_dir.mkdir(parents=True, exist_ok=True)
        self.console.print(f"Using {self.repo_dir} to create Debian mirror")

        try:
            self.console.print("Creating distrobution configuration.")
            repo_dir = self.repo_dir.joinpath("conf")
            repo_dir.mkdir(parents=True, exist_ok=True)
            repo_conf = repo_dir.joinpath("distributions")
            distributions = textwrap.dedent(f"""\
                    Origin: {pocket}
                    Label: StarlingX project udpates
                    Codename: {distro}
                    Architectures: amd64
                    Components: {pocket}
                    Description: Apt repository for StarlingX updates
                    """)
            with open(repo_conf, "w") as outfile:
                outfile.write(distributions)

            self.console.print("Creating options configuration.")
            options_conf = repo_dir.joinpath("options")
            options = textwrap.dedent(f"""\
            basedir {self.repo_dir}
            """)
            with open(options_conf, "w") as outfile:
                outfile.write(options)

        except Exception as e:
            self.console.print(e)

    def add_package(self, repo, suite, package):
        self.console.print(f"Adding {package} to the archive")
        subprocess.run(
            ["reprepro", "-b", repo, "includedeb", suite, package],
            check=True)

    def list_packages(self, repo, suite):
        table = Table()
        table.add_column("Package")
        table.add_column("Version")
        table.add_column("Suite")
        table.add_column("Pocket")
        table.add_column("Architecture")
        out = subprocess.check_output(
            ["reprepro", "-b", repo, "list", suite],
            encoding="utf-8",
        )
        for line in out.splitlines():
            (metadata, package, version) = line.split()
            (suite,pocket,arch) = metadata.split("|")
            table.add_row(package, version, suite, pocket, arch[:-1])

        self.console.print(table)

