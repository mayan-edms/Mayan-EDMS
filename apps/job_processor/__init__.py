from __future__ import absolute_import

import atexit
import logging
from multiprocessing import active_children

from django.db import transaction, DatabaseError
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from scheduler.api import LocalScheduler
from navigation.api import bind_links, register_model_list_columns
from project_tools.api import register_tool
from project_setup.api import register_setup
from common.utils import encapsulate

from clustering.models import Node
from clustering.signals import node_died, node_heartbeat

from .models import JobQueue, JobProcessingConfig, JobQueueItem
from .tasks import job_queue_poll
from .links import (node_workers, job_queues, tool_link,
    job_queue_items_pending, job_queue_items_error, job_queue_items_active,
    job_queue_config_edit, setup_link, job_queue_start, job_queue_stop,
    job_requeue, job_delete)

logger = logging.getLogger(__name__)


@transaction.commit_on_success
def add_job_queue_jobs():
    job_processor_scheduler = LocalScheduler('job_processor', _(u'Job processor'))
    try:
        job_processor_scheduler.add_interval_job('job_queue_poll', _(u'Poll a job queue for pending jobs.'), job_queue_poll, seconds=JobProcessingConfig.get().job_queue_poll_interval)
    except DatabaseError:
        transaction.rollback()

    job_processor_scheduler.start()


add_job_queue_jobs()
register_tool(tool_link)
register_setup(setup_link)
bind_links([JobQueue, 'job_queues'], [job_queues], menu_name='secondary_menu')
bind_links([JobQueue], [job_queue_start, job_queue_stop, job_queue_items_pending, job_queue_items_active, job_queue_items_error])
bind_links([Node], [node_workers])
bind_links(['job_queue_config_edit'], [job_queue_config_edit], menu_name='secondary_menu')
bind_links([JobQueueItem], [job_requeue, job_delete])

Node.add_to_class('workers', lambda node: node.worker_set)

register_model_list_columns(Node, [
    {
        'name': _(u'active workers'),
        'attribute': encapsulate(lambda x: x.workers().all().count())
    },
])


@receiver(node_died, dispatch_uid='process_dead_workers')
def process_dead_workers(sender, **kwargs):
    logger.debug('kwargs')
    logger.debug(kwargs)


@receiver(node_heartbeat, dispatch_uid='node_processes')
def node_processes(sender, **kwargs):
    logger.debug('kwargs')
    logger.debug(kwargs)
    print "PROCS"
    for process in active_children():
        print process.pid


def kill_all_node_processes():
    logger.debug('terminating this node\'s all processes')
    for process in active_children():
        process.terminate()
        process.join()


atexit.register(kill_all_node_processes)
