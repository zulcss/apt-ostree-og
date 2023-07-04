import logging
import os
import subprocess
import sys

from textwrap import dedent

from apt_ostree import constants
from apt_ostree.log import complete_step
from apt_ostree.log import log_step


def run_mmdebstrap(suite, mirror, rootfs, workspace):
    """Running mmdebstrap."""
    components = ["main", "non-free", "contrib"]
    with complete_step("Checking bootstrap configuraiton"):
        log_step(f"Found debian mirror: {mirror}")

        log_step("Checking for suite")
        if suite not in constants.SUITES:
            logging.error(f"{suite} is not valid suite")
            sys.exit(-1)
        log_step(f"Found {suite} version")

    with complete_step("Running mmdebstrap"):
        log_step("Determining bootstrap configuration")

        cmd = ["mmdebstrap", "--verbose"]
        with complete_step("Building mmdebstrap from configuration file"):
            log_step("Including addtional packages")
            cmd += [f"--include={package}"
                    for package in constants.PACKAGES]
            log_step("Including additinal components...")
            cmd + [f"--component={component}"
                   for component in components]
            mirror = _create_mirror(workspace, suite)
            cmd += [suite, str(rootfs), str(mirror)]

            try:
                log_step(f" Running {' '.join(cmd)}")
                subprocess.check_call(cmd)
            except Exception as ex:
                logging.error(f"Failed to run mmdebstrap: {ex}")
                raise ex


def _create_mirror(workspace, suite):
    """Create tempfile with udpates if needed"""
    repo = workspace.joinpath("sources.list")
    if repo.exists():
        os.unlink(repo)
    repo.write_text(
        dedent(
            f"""\
            deb http://deb.debian.org/debian {suite} main
            deb-src http://deb.debian.org/debian {suite} main

            deb http://deb.debian.org/debian-security/ {suite}-security main
            deb-src http://deb.debian.org/debian-security/ {suite}-security main

            deb http://deb.debian.org/debian {suite}-updates main
            deb-src http://deb.debian.org/debian {suite}-updates main
             """
        )
    )
    return repo
