import os
import shutil
import subprocess

from apt_ostree.log import complete_step
from apt_ostree.log import log_step


def run_vm(branch, repo, image, image_size, workspace, suite, template):
    with complete_step("Creating vm"):
        subprocess.check_call(["debos",
                               "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", f"image:{image}",
                               "-t", f"size:{image_size}",
                               "-t", "architecture:amd64",
                               "-t", f"suite:{suite}",
                               template], cwd=workspace)
