from __future__ import absolute_import

from functools import wraps

from . import logger
from . import Lock
from .exceptions import LockError

    
def simple_locking(lock_id, expiration=None):
    """
    A decorator that wraps a function in a single lock getting algorithm
    """
    def inner_decorator(function):
        def wrapper(*args, **kwargs):
            try:
                # Trying to acquire lock
                lock = Lock.acquire_lock(lock_id, expiration)
            except LockError:
                # Unable to acquire lock
                pass
            except Exception:
                # Unhandled error, release lock
                lock.release()
                raise
            else:
                # Lock acquired, proceed normally, release lock afterwards
                logger.debug('acquired lock: %s' % lock_id)
                result = function(*args, **kwargs)
                lock.release()
                return result
        return wraps(function)(wrapper)
    return inner_decorator
