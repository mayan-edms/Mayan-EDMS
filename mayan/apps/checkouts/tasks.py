from __future__ import unicode_literals

import logging

from lock_manager import Lock, LockError
from mayan.celery import app

from .literals import CHECKOUT_EXPIRATION_LOCK_EXPIRE
from .models import DocumentCheckout

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_check_expired_check_outs():
    logger.debug('executing...')
    lock_id = 'task_expired_check_outs'
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        lock = Lock.acquire_lock(
            name=lock_id, timeout=CHECKOUT_EXPIRATION_LOCK_EXPIRE
        )
        logger.debug('acquired lock: %s', lock_id)
        DocumentCheckout.objects.check_in_expired_check_outs()
        lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
