import redis

from django.utils.encoding import force_text

from mayan.apps.dependencies.exceptions import DependenciesException

from ..exceptions import LockError
from ..settings import setting_backend_arguments

from .base import LockingBackend
from .literals import REDIS_LOCK_VERSION_REQUIRED

SCAN_KEYS_COUNT = 5000
REDIS_LOCK_NAME_PREFIX = '_mayan_lock:'


class RedisLock(LockingBackend):
    @classmethod
    def _acquire_lock(cls, name, timeout):
        return RedisLock(name=name, timeout=timeout)

    @classmethod
    def get_redis_connection(cls):
        redis_url = setting_backend_arguments.value.get('redis_url', None)
        server = redis.from_url(url=redis_url)
        # Force to initialize the connection.
        server.client()
        return server

    @classmethod
    def _purge_locks(cls):
        cache = cls.get_redis_connection()

        cursor = '0'
        while True:
            cursor, keys = cache.scan(
                count=SCAN_KEYS_COUNT, cursor=cursor, match='{}*'.format(
                    REDIS_LOCK_NAME_PREFIX
                )
            )
            if keys:
                cache.delete(*keys)

            if cursor == 0:
                break

    def __init__(self, name, timeout):
        if redis.VERSION < REDIS_LOCK_VERSION_REQUIRED:
            raise DependenciesException(
                'The Redis lock backend requires the Redis Python client '
                'version {} or later.'.format(
                    '.'.join(map(force_text, REDIS_LOCK_VERSION_REQUIRED))
                )
            )

        self.name = name
        redis_lock_instance = self.__class__.get_redis_connection().lock(
            name='{}{}'.format(REDIS_LOCK_NAME_PREFIX, name),
            timeout=timeout
        )
        if redis_lock_instance.acquire(blocking=False):
            self.redis_lock_instance = redis_lock_instance
        else:
            raise LockError

    def _release(self):
        try:
            self.redis_lock_instance.release()
        except redis.exceptions.LockNotOwnedError:
            return
