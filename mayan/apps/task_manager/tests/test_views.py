from mayan.apps.tests.tests.base import GenericViewTestCase

from ..classes import Worker, CeleryQueue
from ..permissions import permission_task_view

from .literals import TEST_QUEUE_LABEL, TEST_QUEUE_NAME, TEST_WORKER_NAME


class TaskManagerTestMixin:
    def _create_test_queue(self):
        self.test_worker = Worker(name=TEST_WORKER_NAME)
        self.test_queue = CeleryQueue(
            label=TEST_QUEUE_LABEL, name=TEST_QUEUE_NAME,
            worker=self.test_worker
        )


class TaskManagerViewTestCase(TaskManagerTestMixin, GenericViewTestCase):
    def setUp(self):
        super(TaskManagerViewTestCase, self).setUp()
        self._create_test_queue()

    def _request_queue_list(self):
        return self.get(
            viewname='task_manager:queue_list', follow=True
        )

    def test_queue_list_view_no_permissions(self):
        response = self._request_queue_list()

        self.assertEqual(response.status_code, 403)

    def test_queue_list_view_with_permissions(self):
        self.grant_permission(permission=permission_task_view)

        response = self._request_queue_list()
        self.assertContains(
            response, text=self.test_queue.name, status_code=200
        )
