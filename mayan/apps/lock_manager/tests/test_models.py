from __future__ import unicode_literals

import time

from django.test import TestCase

from ..exceptions import LockError
from ..models import Lock


class LockTestCase(TestCase):
    def test_exclusive(self):
        lock_1 = Lock.objects.acquire_lock(name='test_lock_1')
        with self.assertRaises(LockError):
            Lock.objects.acquire_lock(name='test_lock_1')

        # Cleanup
        lock_1.release()

    def test_release(self):
        lock_1 = Lock.objects.acquire_lock(name='test_lock_1')
        lock_1.release()
        lock_2 = Lock.objects.acquire_lock(name='test_lock_1')

        # Cleanup
        lock_2.release()

    def test_timeout_expired(self):
        Lock.objects.acquire_lock(name='test_lock_1', timeout=1)

        # lock_1 not release and not expired, should raise LockError
        with self.assertRaises(LockError):
            Lock.objects.acquire_lock(name='test_lock_1')

        time.sleep(2)
        # lock_1 not release but has expired, should not raise LockError
        lock_2 = Lock.objects.acquire_lock(name='test_lock_1')

        # Cleanup
        lock_2.release()

    def test_double_release(self):
        lock_1 = Lock.objects.acquire_lock(name='test_lock_1')
        lock_1.release()

    def test_release_expired(self):
        lock_1 = Lock.objects.acquire_lock(name='test_lock_1', timeout=1)
        time.sleep(2)
        lock_1.release()
        # No exception is raised even though the lock has expired.
        # The logic is that checking for expired locks during release is
        # not necesary as any attempt by someone else to aquire the lock
        # would be successfull, even after an extended lapse of time

    def test_release_expired_reaquired(self):
        time.sleep(2)
        lock_2 = Lock.objects.acquire_lock(name='test_lock_1', timeout=1)

        # Cleanup
        lock_2.release()
