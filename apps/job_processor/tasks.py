from __future__ import absolute_import

from datetime import timedelta, datetime
import platform
import logging
import psutil

from lock_manager import Lock, LockError

from .models import Node, JobQueue
from .exceptions import JobQueueNoPendingJobs

LOCK_EXPIRE = 10
# TODO: Tie LOCK_EXPIRATION with hard task timeout

logger = logging.getLogger(__name__)


def refresh_node():
    logger.debug('starting')

    lock_id = u'refresh_node'
    try:
        logger.debug('trying to acquire lock: %s' % lock_id)
        lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s' % lock_id)
        node, created = Node.objects.get_or_create(hostname=platform.node(), defaults={'memory_usage': 0.0})
        node.cpuload = psutil.cpu_percent()
        node.memory_usage = psutil.phymem_usage().percent
        node.save()
        lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
    except Exception:
        lock.release()
        raise


def job_queue_poll():
    logger.debug('starting')

    lock_id = u'job_queue_poll'
    try:
        logger.debug('trying to acquire lock: %s' % lock_id)
        lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s' % lock_id)
        for job_queue in JobQueue.objects.all():
            try:
                job_item = job_queue.get_oldest_pending_job()
                job_item.run()
            except JobQueueNoPendingJobs:
                logger.debug('no pending jobs for job queue: %s' % job_queue)
        lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
    except Exception:
        lock.release()
        raise
