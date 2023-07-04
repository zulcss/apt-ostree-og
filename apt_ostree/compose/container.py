import subprocess

from apt_ostree.log import complete_step
from apt_ostree.log import log_step


def create_container(branch, repo, name, workspace):
    with complete_step("Encapsulating and pushing to docker quay.io"):
        log_step(f"Uploading {name}, please wait")
        name = f"docker://quay.io/{name}"
        repo = workspace.joinpath(repo)
        subprocess.check_call(
            ["ostree", "container", "encapsulate", f"--repo={repo}",
             branch, name])
