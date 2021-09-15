import redis

from django.utils.encoding import force_text

from mayan.apps.dependencies.exceptions import DependenciesException

from ..exceptions import LockError
from ..settings import setting_backend_arguments

from .base import LockingBackend
from .literals import (
    REDIS_LOCK_NAME_PREFIX, REDIS_LOCK_VERSION_REQUIRED,
    REDIS_SCAN_KEYS_COUNT, REDIS_USE_CONNECTION_POOL
)


class RedisLock(LockingBackend):
    @classmethod
    def _acquire_lock(cls, name, timeout):
        return RedisLock(name=name, timeout=timeout)

    @classmethod
    def _initialize(cls):
        if REDIS_USE_CONNECTION_POOL:
            redis_url = setting_backend_arguments.value.get('redis_url', None)
            cls._connection_pool = redis.ConnectionPool.from_url(url=redis_url)

    @classmethod
    def get_redis_connection(cls):
        if REDIS_USE_CONNECTION_POOL:
            server = redis.Redis(connection_pool=cls._connection_pool)
        else:
            redis_url = setting_backend_arguments.value.get('redis_url', None)
            server = redis.from_url(url=redis_url)
            # Force to initialize the connection.
            server.client()
        return server

    @classmethod
    def _purge_locks(cls):
        server = cls.get_redis_connection()

        cursor = '0'
        while True:
            cursor, keys = server.scan(
                count=REDIS_SCAN_KEYS_COUNT, cursor=cursor, match='{}*'.format(
                    REDIS_LOCK_NAME_PREFIX
                )
            )
            if keys:
                server.delete(*keys)

            if cursor == 0:
                break

    def _init(self, name, timeout):
        if redis.VERSION < REDIS_LOCK_VERSION_REQUIRED:
            raise DependenciesException(
                'The Redis lock backend requires the Redis Python client '
                'version {} or later.'.format(
                    '.'.join(map(force_text, REDIS_LOCK_VERSION_REQUIRED))
                )
            )

        self.name = name
        _redis_lock_instance = self.__class__.get_redis_connection().lock(
            name='{}{}'.format(REDIS_LOCK_NAME_PREFIX, name),
            timeout=timeout
        )
        if _redis_lock_instance.acquire(blocking=False):
            self._redis_lock_instance = _redis_lock_instance
        else:
            raise LockError

    def _release(self):
        try:
            self._redis_lock_instance.release()
        except redis.exceptions.LockNotOwnedError:
            return
