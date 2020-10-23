import time

from unittest import skip
from django.test import override_settings
from django.utils.module_loading import import_string

from mayan.apps.testing.tests.base import BaseTestCase

from ..exceptions import LockError

TEST_LOCK_1 = 'test lock 1'


class FileLockTestCase(BaseTestCase):
    backend_string = 'mayan.apps.lock_manager.backends.file_lock.FileLock'

    def setUp(self):
        super(FileLockTestCase, self).setUp()
        self.locking_backend = import_string(dotted_path=self.backend_string)

    def test_exclusive(self):
        lock_1 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)
        with self.assertRaises(expected_exception=LockError):
            self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_1.release()

    def test_release(self):
        lock_1 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)
        lock_1.release()
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_2.release()

    def test_timeout_expired(self):
        self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)

        # lock_1 not release and not expired, should raise LockError
        with self.assertRaises(expected_exception=LockError):
            self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        time.sleep(1.01)
        # lock_1 not release but has expired, should not raise LockError
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_2.release()

    def test_double_release(self):
        lock_1 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)
        lock_1.release()

    def test_release_expired(self):
        lock_1 = self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)
        time.sleep(1.01)
        lock_1.release()
        # No exception is raised even though the lock has expired.
        # The logic is that checking for expired locks during release is
        # not necessary as any attempt by someone else to aquire the lock
        # would be successfull, even after an extended lapse of time

    def test_release_expired_reaquired(self):
        self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)
        time.sleep(1.01)
        # TEST_LOCK_1 is expired so trying to acquire it should not return an
        # error.
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)

        # Cleanup
        lock_2.release()


class ModelLockTestCase(FileLockTestCase):
    backend_string = 'mayan.apps.lock_manager.backends.model_lock.ModelLock'


@skip('Skip until a Mock Redis server class is added.')
@override_settings(
    LOCK_MANAGER_BACKEND_ARGUMENTS={'redis_url': 'redis://127.0.0.1:6379/0'}
)
class RedisLockTestCase(FileLockTestCase):
    backend_string = 'mayan.apps.lock_manager.backends.redis_lock.RedisLock'
