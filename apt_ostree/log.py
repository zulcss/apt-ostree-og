# vim: tabstop=4 shiftwidth=4 softtabstop=4

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import contextlib
import logging
import os
import sys
from typing import Any

LEVEL = 0


def log_step(text):
    prefix = " " * LEVEL
    if sys.exc_info()[0]:
        logging.info(f"{prefix}({text})")
    else:
        logging.info(f"{prefix}{Style.bold}{text}{Style.reset}")


@contextlib.contextmanager
def complete_step(text, text2=None):
    global LEVEL

    log_step(text)

    LEVEL += 1
    try:
        args: list[Any] = []
        yield args
    finally:
        LEVEL -= 1
        assert LEVEL >= 0

    if text2 is not None:
        log_step(text2.format(*args))


class Style:
    bold = "\033[0;1;39m" if sys.stderr.isatty() else ""
    gray = "\x1b[38;20m" if sys.stderr.isatty() else ""
    red = "\033[31;1m" if sys.stderr.isatty() else ""
    yellow = "\033[33;1m" if sys.stderr.isatty() else ""
    reset = "\033[0m" if sys.stderr.isatty() else ""


class OstreeFormatter(logging.Formatter):
    def __init__(self, fmt=None, *args, **kwargs):
        fmt = fmt or "%(message)s"

        self.formatters = {
            logging.DEBUG: logging.Formatter(
                f"* {Style.gray}{fmt}{Style.reset}"),
            logging.INFO: logging.Formatter(
                f"* {fmt}"),
            logging.WARNING: logging.Formatter(
                f"* {Style.yellow}{fmt}{Style.reset}"),
            logging.ERROR: logging.Formatter(
                f"* {Style.red}{fmt}{Style.reset}"),
            logging.CRITICAL: logging.Formatter(
                f"* {Style.red}{Style.bold}{fmt}{Style.reset}"),
        }

        super().__init__(fmt, *args, **kwargs)

    def format(self, record):
        return self.formatters[record.levelno].format(record)


def setup_log():
    handler = logging.StreamHandler(stream=sys.stderr)

    level = logging.getLevelName(
        os.getenv("SYSTEMD_LOG_LEVEL", "info").upper())
    handler.setFormatter(OstreeFormatter())

    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level)
