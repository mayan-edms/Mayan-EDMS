from __future__ import unicode_literals

import redis

from django.utils.encoding import force_text

from mayan.apps.dependencies.exceptions import DependenciesException

from ..exceptions import LockError
from ..settings import setting_backend_arguments

from .base import LockingBackend
from .literals import REDIS_LOCK_VERSION_REQUIRED


class RedisLock(LockingBackend):
    @classmethod
    def acquire_lock(cls, name, timeout=None):
        super(RedisLock, cls).acquire_lock(name=name, timeout=timeout)
        return RedisLock(name=name, timeout=timeout)

    @classmethod
    def get_redis_connection(cls):
        redis_url = setting_backend_arguments.value.get('redis_url', None)
        server = redis.from_url(url=redis_url)
        # Force to initialize the connection
        server.client()
        return server

    @classmethod
    def purge_locks(cls):
        super(RedisLock, cls).purge_locks()

    def __init__(self, name, timeout):
        if redis.VERSION < REDIS_LOCK_VERSION_REQUIRED:
            raise DependenciesException(
                'The Redis lock backend requires the Redis Python client '
                'version {} or later.'.format(
                    '.'.join(map(force_text, REDIS_LOCK_VERSION_REQUIRED))
                )
            )

        self.name = name
        redis_lock_instance = self.get_redis_connection().lock(
            name=name, timeout=timeout, sleep=0.1, blocking_timeout=0.1
        )
        if redis_lock_instance.acquire():
            self.redis_lock_instance = redis_lock_instance
        else:
            raise LockError

    def release(self):
        super(RedisLock, self).release()
        try:
            self.redis_lock_instance.release()
        except redis.exceptions.LockNotOwnedError:
            return
