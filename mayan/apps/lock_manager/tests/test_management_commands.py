from unittest import skip

from django.test import override_settings

from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import (
    LockBackendManagementCommandTestCaseMixin, LockBackendTestMixin
)


class FileLockBackendManagementCommandTestCase(
    LockBackendTestMixin, LockBackendManagementCommandTestCaseMixin,
    BaseTestCase
):
    backend_string = 'mayan.apps.lock_manager.backends.file_lock.FileLock'


class ModelLockBackendManagementCommandTestCase(
    LockBackendTestMixin, LockBackendManagementCommandTestCaseMixin,
    BaseTestCase
):
    backend_string = 'mayan.apps.lock_manager.backends.model_lock.ModelLock'


@skip('Skip until a Mock Redis server class is added.')
@override_settings(
    LOCK_MANAGER_BACKEND_ARGUMENTS={'redis_url': 'redis://127.0.0.1:6379/0'}
)
class RedisLockBackendManagementCommandTestCase(
    LockBackendTestMixin, LockBackendManagementCommandTestCaseMixin,
    BaseTestCase
):
    backend_string = 'mayan.apps.lock_manager.backends.redis_lock.RedisLock'
