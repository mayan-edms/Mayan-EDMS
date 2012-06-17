from __future__ import absolute_import

import logging

from lock_manager import Lock, LockError

from .models import DocumentCheckout

LOCK_EXPIRE = 50
logger = logging.getLogger(__name__)


def task_check_expired_check_outs():
    logger.debug('executing...')
    lock_id = u'task_expired_check_outs'
    try:
        logger.debug('trying to acquire lock: %s' % lock_id)
        lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s' % lock_id)
        DocumentCheckout.objects.check_in_expired_check_outs()
        lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
        pass
