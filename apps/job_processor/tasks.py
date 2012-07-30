from __future__ import absolute_import

import logging

from lock_manager import Lock, LockError
from clustering.models import Node

from .models import JobQueue
from .exceptions import JobQueueNoPendingJobs

LOCK_EXPIRE = 10
MAX_CPU_LOAD = 90.0
MAX_MEMORY_USAGE = 90.0

logger = logging.getLogger(__name__)


def job_queue_poll():
    logger.debug('starting')

    node = Node.objects.myself()  # Automatically calls the refresh() method too
    if node.cpuload < MAX_CPU_LOAD and node.memory_usage < MAX_MEMORY_USAGE:
        # Poll job queues if node is not overloaded
        lock_id = u'job_queue_poll'
        try:
            lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        except LockError:
            pass
        except Exception:
            lock.release()
            raise
        else:
            for job_queue in JobQueue.objects.all():
                try:
                    job_item = job_queue.get_oldest_pending_job()
                    job_item.run()
                except JobQueueNoPendingJobs:
                    logger.debug('no pending jobs for job queue: %s' % job_queue)
            lock.release()
            
