from ..classes import Worker, CeleryQueue

from .literals import TEST_QUEUE_LABEL, TEST_QUEUE_NAME, TEST_WORKER_NAME


class TaskManagerTestMixin:
    def _create_test_queue(self):
        self.test_worker = Worker(name=TEST_WORKER_NAME)
        self.test_queue = CeleryQueue(
            label=TEST_QUEUE_LABEL, name=TEST_QUEUE_NAME,
            worker=self.test_worker
        )


class TaskManagerViewTestMixin:
    def _request_queue_list(self):
        return self.get(
            viewname='task_manager:queue_list', follow=True
        )
