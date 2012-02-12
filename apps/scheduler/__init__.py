from __future__ import absolute_import

import logging

from .runtime import scheduler

from django.db.models.signals import post_syncdb
from django.dispatch import receiver

from signaler.signals import pre_collectstatic

logger = logging.getLogger(__name__)


@receiver(post_syncdb, dispatch_uid='scheduler_shutdown_post_syncdb')
def scheduler_shutdown_post_syncdb(sender, **kwargs):
    logger.debug('Scheduler shut down on post syncdb signal')
    scheduler.shutdown()


@receiver(pre_collectstatic, dispatch_uid='sheduler_shutdown_pre_collectstatic')
def sheduler_shutdown_pre_collectstatic(sender, **kwargs):
    logger.debug('Scheduler shut down on collectstatic signal')
    scheduler.shutdown()
