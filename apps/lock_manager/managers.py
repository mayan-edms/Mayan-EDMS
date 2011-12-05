import logging
import datetime

from django.db.utils import DatabaseError
from django.db.utils import IntegrityError
from django.db import transaction
from django.db import models

from lock_manager.exceptions import LockError

logger = logging.getLogger(__name__)


class LockManager(models.Manager):
    @transaction.commit_on_success
    def acquire_lock(self, name, timeout=None):
        logger.debug('trying to acquire lock: %s' % name)
        lock = self.model(name=name, timeout=timeout)
        try:
            lock.save(force_insert=True)
            logger.debug('acquired lock: %s' % name)
            return lock
        except IntegrityError, msg:
            logger.debug('IntegrityError: %s', msg)
            # There is already an existing lock
            # Check it's expiration date and if expired, reset it
            try:
                lock = self.model.objects.get(name=name)
            except self.model.DoesNotExist:
                # Table based locking
                logger.debug('lock: %s does not exist' % name)
                raise LockError('Unable to acquire lock')

            if datetime.datetime.now() > lock.creation_datetime + datetime.timedelta(seconds=lock.timeout):
                logger.debug('reseting deleting stale lock: %s' % name)
                lock.timeout = timeout
                logger.debug('trying to reacquire stale lock: %s' % name)
                lock.save()
                logger.debug('reacquired stale lock: %s' % name)
                return lock
            else:
                logger.debug('unable to acquire lock: %s' % name)
                raise LockError('Unable to acquire lock')
