import logging
import os
import pathlib
import shutil

import click

from apt_ostree.config import Config
from apt_ostree.cmd.compose import options
from apt_ostree.compose import bootstrap
from apt_ostree.compose import ostree
from apt_ostree.compose import vm
from apt_ostree import constants
from apt_ostree.log import complete_step
from apt_ostree.log import log_step
from apt_ostree.log import setup_log
from apt_ostree import preflight


@click.command(help="Compose an image")
@click.pass_context
@options.config
def image(ctxt, config):
    setup_log()

    # default mirror
    mirror = "http://deb.debain.org/debian"

    workspace = constants.WORKSPACE
    with complete_step(f"Setting up workspace {constants.WORKSPACE}"):
        workspace = constants.WORKSPACE
        if workspace.exists():
            shutil.rmtree(workspace)
        log_step(f"{workspace} does not exist, creating")
        shutil.copytree(config, workspace)

        output = pathlib.Path(constants.ARTIFACT)
    
        c = Config()
        config = c.load_config(config)
        suite = config.get("suite")
        branch = config.get("branch")
        repo = config.get("repo")
        ostree_template = config.get("ostree_template")
        name = config.get("name")
        image_size = config.get("size")
        image_template = config.get("image_template")


        try:
            # Check for required programs
            preflight.preflight_check()

            # Run mmdebstrap to build the rootfs.tar.gz
            rootfs = workspace.joinpath(output)
            if rootfs.exists():
                os.unlink(rootfs)
            bootstrap.run_mmdebstrap(
                suite, mirror, rootfs, workspace)

            # Create ostree repo
            ostree.create_ostree_repo(rootfs, workspace, repo)

            # Commit rootfs to repo
            ostree.create_ostree_commit(
                workspace, branch, repo,  suite, ostree_template)

            # Run debos to create the image
            vm.run_vm(branch, repo, name, image_size, workspace,  suite, image_template)

        except Exception as ex:
            logging.error(f"Failed to compose: {ex}")
            raise ex
