from __future__ import unicode_literals


class LockingBackend(object):
    """
    Base class for the lock backends. Defines the base methods that each
    subclass must define.
    """
    @classmethod
    def acquire_lock(cls, name, timeout=None):
        raise NotImplementedError

    @classmethod
    def purge_locks(cls):
        raise NotImplementedError
