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


def create_ostree_commit(workspace, branch, repo, suite, template):
    with complete_step("Commiting rootfs to ostree"):

        logging.info(template)

        subprocess.check_call(["debos",
                              "-v",
                               "-t", f"branch:{branch}",
                               "-t", f"repo:{repo}",
                               "-t", "architecture:amd64",
                               "-t", f"suite:{suite}",
                               template], cwd=workspace)
