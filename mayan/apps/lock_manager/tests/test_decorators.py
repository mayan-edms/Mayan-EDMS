from unittest import skip

from django.test import override_settings
from django.utils.module_loading import import_string

from mayan.apps.testing.tests.base import BaseTestCase

from ..decorators import locked_class_method
from ..exceptions import LockError

from .literals import TEST_LOCK_1


class FileLockDecoratorTestCase(BaseTestCase):
    backend_string = 'mayan.apps.lock_manager.backends.file_lock.FileLock'

    def setUp(self):
        super().setUp()
        self.locking_backend = import_string(dotted_path=self.backend_string)

    def test_decorator_single_class(self):
        class TestClass:
            def _lock_manager_get_lock_name(self, *args, **kwargs):
                return TEST_LOCK_1

            @locked_class_method
            def method_1(self, _acquire_lock=True):
                """Locked parent method"""
                self.method_2()

            @locked_class_method
            def method_2(self, _acquire_lock=True):
                """Locked child method"""

        test_object = TestClass()
        with self.assertRaises(expected_exception=LockError):
            test_object.method_1()

    def test_decorator_multiple_classes(self):
        class TestClass1:
            def _lock_manager_get_lock_name(self, *args, **kwargs):
                return TEST_LOCK_1

            @locked_class_method
            def method_1(self, _acquire_lock=True):
                test_object_2 = TestClass2()
                test_object_2.method_1()

        class TestClass2:
            def _lock_manager_get_lock_name(self, *args, **kwargs):
                """Locked parent class method"""
                return TEST_LOCK_1

            @locked_class_method
            def method_1(self, _acquire_lock=True):
                """Locked child class method"""

        test_object_1 = TestClass1()

        with self.assertRaises(expected_exception=LockError):
            test_object_1.method_1()


class ModelLockTestCase(FileLockDecoratorTestCase):
    backend_string = 'mayan.apps.lock_manager.backends.model_lock.ModelLock'


@skip('Skip until a Mock Redis server class is added.')
@override_settings(
    LOCK_MANAGER_BACKEND_ARGUMENTS={'redis_url': 'redis://127.0.0.1:6379/0'}
)
class RedisLockTestCase(FileLockDecoratorTestCase):
    backend_string = 'mayan.apps.lock_manager.backends.redis_lock.RedisLock'
