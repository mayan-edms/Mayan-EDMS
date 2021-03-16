import logging

from django.utils.module_loading import import_string

from ..settings import setting_backend, setting_default_lock_timeout

logger = logging.getLogger(name=__name__)


class LockingBackend:
    """
    Base class for the lock backends. Defines the base methods that each
    subclass must define.
    """
    @staticmethod
    def get_instance():
        return import_string(dotted_path=setting_backend.value)

    @classmethod
    def acquire_lock(cls, name, timeout=None):
        timeout = timeout or setting_default_lock_timeout.value
        logger.debug('acquiring lock: %s, timeout: %s', name, timeout)
        return cls._acquire_lock(name=name, timeout=timeout)

    @classmethod
    def purge_locks(cls):
        logger.debug('purging locks')
        return cls._purge_locks()

    def release(self):
        logger.debug('releasing lock: %s', self.name)
        return self._release()
