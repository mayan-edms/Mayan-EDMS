import functools
import inspect
import logging

from django.core.exceptions import ImproperlyConfigured

from .backends.base import LockingBackend
from .exceptions import LockError

logger = logging.getLogger(name=__name__)


def locked_class_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if inspect.isgeneratorfunction(getattr(func, '__wrapped__', None)):
            raise ImproperlyConfigured(
                'This decorator does not support generators.'
            )

        _acquire_lock = kwargs.pop('_acquire_lock', True)
        lock_name = self._lock_manager_get_lock_name(*args, **kwargs)

        try:
            if _acquire_lock:
                logger.debug('trying to acquire lock: %s', lock_name)
                lock = LockingBackend.get_backend().acquire_lock(name=lock_name)
                logger.debug('acquired lock: %s', lock_name)
        except LockError:
            logger.debug('unable to obtain lock: %s' % lock_name)
            raise
        else:
            try:
                return func(self, *args, **kwargs)
            finally:
                if _acquire_lock:
                    lock.release()
    return wrapper


def acquire_lock_class_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if inspect.isgeneratorfunction(getattr(func, '__wrapped__', None)):
            raise ImproperlyConfigured(
                'This decorator does not support generators.'
            )

        _acquire_lock = kwargs.pop('_acquire_lock', True)
        lock_name = self._lock_manager_get_lock_name(*args, **kwargs)

        try:
            if _acquire_lock:
                logger.debug('trying to acquire lock: %s', lock_name)
                self._lock = LockingBackend.get_backend().acquire_lock(name=lock_name)
                logger.debug('acquired lock: %s', lock_name)
        except LockError:
            logger.debug('unable to obtain lock: %s' % lock_name)
            raise
        else:
            return func(self, *args, **kwargs)

    return wrapper


def release_lock_class_method(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if inspect.isgeneratorfunction(getattr(func, '__wrapped__', None)):
            raise ImproperlyConfigured(
                'This decorator does not support generators.'
            )

        _acquire_lock = kwargs.pop('_acquire_lock', True)

        try:
            return func(self, *args, **kwargs)
        finally:
            if _acquire_lock:
                self._lock.release()
    return wrapper
