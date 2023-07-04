import os
import shutil
import subprocess

from apt_ostree.log import complete_step
from apt_ostree.log import log_step


def run_vm(branch, repo, image, image_size, workspace, arch, suite):
    with complete_step("Setting up workspace for image creation"):
        log_step("Copying apt_ostree scripts to workspace")

        log_step("Copying ostree-uefi-amd64.yaml configuration to workspace")
        config = os.path.join(os.path.dirname(__file__),
                              "templates", f'debian-ostree-{arch}.yaml')
        template = workspace.joinpath(f'debian-ostree-{arch}.yaml')
        shutil.copyfile(config, template)

    with complete_step("Creating vm"):
        subprocess.check_call(["debos",
                               "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", f"image:{image}",
                               "-t", f"size:{image_size}",
                               "-t", f"sarchitecture:{arch}",
                               "-t", f"suite:{suite}",
                               template], cwd=workspace)
