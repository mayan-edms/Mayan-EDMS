import logging

from django.utils.module_loading import import_string

from ..settings import setting_backend, setting_default_lock_timeout

logger = logging.getLogger(name=__name__)


class LockingBackend:
    """
    Base class for the lock backends. Defines the base methods that each
    subclass must define.
    """
    _is_initialized = False

    @classmethod
    def _initialize(cls):
        """
        Optional class method for subclasses to overload.
        """
        return

    @staticmethod
    def get_backend():
        return import_string(dotted_path=setting_backend.value)

    @classmethod
    def acquire_lock(cls, name, timeout=None):
        timeout = timeout or setting_default_lock_timeout.value
        logger.debug('acquiring lock: %s, timeout: %s', name, timeout)
        return cls._acquire_lock(name=name, timeout=timeout)

    @classmethod
    def purge_locks(cls):
        if not cls._is_initialized:
            cls._initialize()
            cls._is_initialized = True

        logger.debug('purging locks')
        return cls._purge_locks()

    def __init__(self, *args, **kwargs):
        if not self.__class__._is_initialized:
            self.__class__._initialize()
            self.__class__._is_initialized = True

        return self._init(*args, **kwargs)

    def release(self):
        logger.debug('releasing lock: %s', self.name)
        return self._release()
