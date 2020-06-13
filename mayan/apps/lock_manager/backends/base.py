import logging

from django.utils.module_loading import import_string

from ..settings import setting_backend

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
        logger.debug('acquiring lock: %s, timeout: %s', name, timeout)

    @classmethod
    def purge_locks(cls):
        logger.debug('purging locks')

    def release(self):
        logger.debug('releasing lock: %s', self.name)
