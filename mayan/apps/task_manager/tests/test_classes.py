from mayan.apps.testing.tests.base import BaseTestCase
from mayan.celery import app as celery_app

from ..classes import CeleryQueue

from .mixins import TaskManagerTestMixin, TaskManagerViewTestMixin


class CeleryQueueTestCase(
    TaskManagerTestMixin, TaskManagerViewTestMixin, BaseTestCase
):
    def test_queue_creation(self):
        CeleryQueue.update_celery()

        test_celery_queue_count = len(celery_app.conf.task_queues)

        self._create_test_queue()
        CeleryQueue.update_celery()

        self.assertTrue(
            len(celery_app.conf.task_queues), test_celery_queue_count + 1
        )

    def test_queue_removal(self):
        self._create_test_queue(
            label='test-queue-unique-1', name='test-queue-unique-1'
        )
        CeleryQueue.update_celery()
        test_celery_queue_count = len(celery_app.conf.task_queues)

        self._test_queue.remove()
        CeleryQueue.update_celery()

        self.assertTrue(
            len(celery_app.conf.task_queues), test_celery_queue_count - 1
        )
