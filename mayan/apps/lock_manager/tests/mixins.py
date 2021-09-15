import os

from django.core import management
from django.utils.module_loading import import_string

from ..exceptions import LockError
from ..settings import setting_default_lock_timeout

from .literals import TEST_LOCK_1


class LockBackendManagementCommandTestCaseMixin:
    def test_purgelocks_command(self):
        self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=20)

        # lock_1 not release and not expired, should raise LockError
        with self.assertRaises(expected_exception=LockError):
            self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        os.environ['MAYAN_LOCK_MANAGER_BACKEND'] = self.backend_string
        management.call_command(command_name='purgelocks')

        # lock_1 not release but has expired, should not raise LockError
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_2.release()


class LockBackendTestMixin:
    def setUp(self):
        super().setUp()
        self.locking_backend = import_string(dotted_path=self.backend_string)


class LockBackendTestCaseMixin:
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

        self._test_delay(seconds=1.01)

        # lock_1 not release but has expired, should not raise LockError
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_2.release()

    def test_double_release(self):
        lock_1 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)
        lock_1.release()

    def test_release_expired(self):
        lock_1 = self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)

        self._test_delay(seconds=1.01)

        lock_1.release()
        # No exception is raised even though the lock has expired.
        # The logic is that checking for expired locks during release is
        # not necessary as any attempt by someone else to aquire the lock
        # would be successfull, even after an extended lapse of time

    def test_release_expired_reaquired(self):
        self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)

        self._test_delay(seconds=1.01)

        # TEST_LOCK_1 is expired so trying to acquire it should not return an
        # error.
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=1)

        # Cleanup
        lock_2.release()

    def test_purge(self):
        self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=30)

        # lock_1 not release and not expired, should raise LockError
        with self.assertRaises(expected_exception=LockError):
            self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        self.locking_backend.purge_locks()

        # lock_1 not release but has expired, should not raise LockError
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_2.release()


class DefaultTimeoutTestMixin:
    def setUp(self):
        super().setUp()
        self.locking_backend = import_string(dotted_path=self.backend_string)
        setting_default_lock_timeout.set(value=1)
        self.assertEqual(setting_default_lock_timeout.value, 1)

    def test_default_timeout_expired(self):
        self.locking_backend.acquire_lock(name=TEST_LOCK_1, timeout=None)

        # lock_1 not release and not expired, should raise LockError
        with self.assertRaises(expected_exception=LockError):
            self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        self._test_delay(seconds=1.01)

        # lock_1 not release but has expired, should not raise LockError
        lock_2 = self.locking_backend.acquire_lock(name=TEST_LOCK_1)

        # Cleanup
        lock_2.release()
