from __future__ import absolute_import

import sys
import logging

from apscheduler.scheduler import Scheduler

from .literals import SHUTDOWN_COMMANDS

logger = logging.getLogger(__name__)
scheduler = Scheduler()

if not any([command in sys.argv for command in SHUTDOWN_COMMANDS]):
    logger.debug('Starting scheduler')
    scheduler.start()


