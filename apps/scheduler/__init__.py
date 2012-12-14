from __future__ import absolute_import

import atexit
import logging
import sys

from navigation.api import bind_links

from .links import scheduler_tool_link, scheduler_list, job_list
from .literals import SHUTDOWN_COMMANDS
from .api import LocalScheduler
from .runtime import scheduler, lockdown

logger = logging.getLogger(__name__)


def schedule_shutdown_on_exit():
    logger.debug('Scheduler shut down on exit')
    LocalScheduler.shutdown_all()
    LocalScheduler.clear_all()


if any([command in sys.argv for command in SHUTDOWN_COMMANDS]):
    logger.debug('Schedulers shut down on SHUTDOWN_COMMAND')
    # Shutdown any scheduler already running
    LocalScheduler.shutdown_all()
    LocalScheduler.clear_all()
    # Prevent any new scheduler afterwards to start
    LocalScheduler.lockdown()

atexit.register(schedule_shutdown_on_exit)
bind_links([LocalScheduler, 'scheduler_list', 'job_list'], scheduler_list, menu_name='secondary_menu')
bind_links([LocalScheduler], job_list)
