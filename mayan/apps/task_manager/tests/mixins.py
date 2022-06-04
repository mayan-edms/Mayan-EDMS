from django_celery_beat.models import IntervalSchedule, PeriodicTask

from ..classes import Worker, CeleryQueue

from .literals import (
    TEST_INTERVAL_SCHEDULE_EVERY, TEST_INTERVAL_SCHEDULE_PERIOD,
    TEST_PERIODIC_TASK_NAME, TEST_PERIODIC_TASK_TASK, TEST_QUEUE_LABEL,
    TEST_QUEUE_NAME, TEST_WORKER_NAME
)


class TaskManagerManagementCommandTestMixin:
    def setUp(self):
        super().setUp()

        self._test_interval_schedule = IntervalSchedule.objects.create(
            every=TEST_INTERVAL_SCHEDULE_EVERY,
            period=TEST_INTERVAL_SCHEDULE_PERIOD
        )
        PeriodicTask.objects.create(
            interval=self._test_interval_schedule,
            name=TEST_PERIODIC_TASK_NAME, task=TEST_PERIODIC_TASK_TASK
        )


class TaskManagerTestMixin:
    def setUp(self):
        super().setUp()
        self._test_queues = []

    def tearDown(self):
        for test_queue in self._test_queues:
            test_queue.remove()

    def _create_test_queue(self, label=None, name=None):
        self.test_worker = Worker(name=TEST_WORKER_NAME)

        total_test_queues = len(self._test_queues)
        label = label or '{}_{}'.format(TEST_QUEUE_LABEL, total_test_queues)
        name = name or '{}_{}'.format(TEST_QUEUE_NAME, total_test_queues)

        self._test_queue = CeleryQueue(
            label=label, name=name, worker=self.test_worker
        )
        self._test_queues.append(self._test_queue)


class TaskManagerViewTestMixin:
    def _request_queue_list(self):
        return self.get(
            viewname='task_manager:queue_list', follow=True
        )
