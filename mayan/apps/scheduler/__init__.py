from __future__ import absolute_import

import atexit
import logging
import sys

from project_tools.api import register_tool

from .links import job_list
from .literals import SHUTDOWN_COMMANDS
from .runtime import scheduler, lockdown

logger = logging.getLogger(__name__)


def schedule_shutdown_on_exit():
    logger.debug('Scheduler shut down on exit')
    scheduler.shutdown()


if any([command in sys.argv for command in SHUTDOWN_COMMANDS]):
    logger.debug('Scheduler shut down on SHUTDOWN_COMMAND')
    # Shutdown any scheduler already running
    scheduler.shutdown()
    # Prevent any new scheduler afterwards to start
    lockdown()


atexit.register(schedule_shutdown_on_exit)
register_tool(job_list)
