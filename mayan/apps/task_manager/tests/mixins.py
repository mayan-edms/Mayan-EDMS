from ..classes import Worker, CeleryQueue

from .literals import TEST_QUEUE_LABEL, TEST_QUEUE_NAME, TEST_WORKER_NAME


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
