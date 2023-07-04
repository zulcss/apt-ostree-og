import logging
import os
import pathlib
import shutil
import subprocess
import sys

from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.utils import run_cmd


def create_ostree_repo(rootfs, workspace, repo):
    with complete_step("Preparing for ostree repository setup"):
        if not rootfs.exists():
            logging.error(f"Unable to find rootfs: {rootfs}")
            sys.exit(-1)

        log_step(f"Creating ostree repo {repo}")
        run_cmd(
            f'ostree init --repo={workspace.joinpath(repo)} --mode=archive')


def create_ostree_commit(workspace, branch, repo, arch, suite):
    with complete_step("Setting up workspace for vm"):
        log_step("Copying apt_ostree scripts to workspace")
        script_dir = pathlib.Path(os.path.join(
            os.path.dirname(__file__), "templates", "scripts"))
        shutil.copytree(script_dir, workspace.joinpath("scripts"))

        log_step("Copying apt_ostree actions to workspace")
        action_dir = pathlib.Path(os.path.join(
            os.path.dirname(__file__), "templates", "actions"))
        shutil.copytree(action_dir, workspace.joinpath("actions"))

        log_step("Copying apt_ostree overlay to workspace")
        overlay_dir = pathlib.Path(os.path.join(
            os.path.dirname(__file__), "templates", "overlay"))
        shutil.copytree(overlay_dir, workspace.joinpath("overlay"))

        log_step("Copying ostree templates configuration to workspace")
        config = os.path.join(os.path.dirname(__file__),
                              "templates", 'debian-ostree-commit.yaml')
        template = workspace.joinpath("debian-ostree-commit.yaml")
        shutil.copyfile(config, template)

    with complete_step("Commiting rootfs to ostree"):

        subprocess.check_call(["debos",
                              "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", f"architecture:{arch}",
                               "-t", f"suite:{suite}",
                               template], cwd=workspace)
