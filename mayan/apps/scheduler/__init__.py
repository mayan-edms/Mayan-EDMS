from __future__ import absolute_import

import atexit
import logging

from .runtime import scheduler
import logging

logger = logging.getLogger(__name__)


def schedule_shutdown_on_exit():
    logger.debug('Scheduler shut down on exit')
    scheduler.shutdown()


atexit.register(schedule_shutdown_on_exit)
