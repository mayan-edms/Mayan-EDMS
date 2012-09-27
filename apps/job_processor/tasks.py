from __future__ import absolute_import

import logging
import psutil

from lock_manager import Lock, LockError
from lock_manager.decorators import simple_locking
from clustering.models import Node

from .models import JobQueue, JobQueueItem
from .exceptions import JobQueueNoPendingJobs
from .literals import JOB_QUEUE_STATE_STARTED
from .settings import MAX_CPU_LOAD, MAX_MEMORY_USAGE, NODE_MAX_WORKERS

logger = logging.getLogger(__name__)


def job_queue_poll():
    logger.debug('starting')

    # Poll job queues if node is not overloaded
    lock_id = u'job_queue_poll'
    try:
        lock = Lock.acquire_lock(lock_id)
    except LockError:
        pass
    else:
        node = Node.objects.myself()
        if node.cpuload < MAX_CPU_LOAD and node.memory_usage < MAX_MEMORY_USAGE and node.worker_set.count() < NODE_MAX_WORKERS:
            for job_queue in JobQueue.objects.filter(state=JOB_QUEUE_STATE_STARTED):
                try:
                    job_item = job_queue.get_oldest_pending_job()
                    job_item.run()
                    break;
                except JobQueueNoPendingJobs:
                    logger.debug('no pending jobs for job queue: %s' % job_queue)
        else:
            logger.debug('CPU load or memory usage over limit')
            lock.release()


@simple_locking('house_keeping', 10)
def house_keeping():
    logger.debug('starting')
    JobQueueItem.objects.check_dead_job_queue_items()
