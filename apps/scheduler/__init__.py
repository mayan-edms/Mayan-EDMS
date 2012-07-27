from __future__ import absolute_import

import logging
import atexit

from .runtime import scheduler

from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from south.signals import pre_migrate

from signaler.signals import pre_collectstatic
from project_tools.api import register_tool

from .links import job_list
    
logger = logging.getLogger(__name__)

@receiver(post_syncdb, dispatch_uid='scheduler_shutdown_post_syncdb')
def scheduler_shutdown_post_syncdb(sender, **kwargs):
    logger.debug('Scheduler shut down on post syncdb signal')
    scheduler.shutdown()


@receiver(pre_collectstatic, dispatch_uid='sheduler_shutdown_pre_collectstatic')
def sheduler_shutdown_pre_collectstatic(sender, **kwargs):
    logger.debug('Scheduler shut down on collectstatic signal')
    scheduler.shutdown()


@receiver(pre_migrate, dispatch_uid='sheduler_shutdown_pre_migrate')
def sheduler_shutdown_pre_migrate(sender, **kwargs):
    logger.debug('Scheduler shut down on pre_migrate signal')
    scheduler.shutdown()


def schedule_shutdown_on_exit():
    logger.debug('Scheduler shut down on exit')
    scheduler.shutdown()


register_tool(job_list)
atexit.register(schedule_shutdown_on_exit)
