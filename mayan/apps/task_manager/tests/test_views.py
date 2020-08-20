from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import permission_task_view

from .mixins import TaskManagerTestMixin, TaskManagerViewTestMixin


class TaskManagerViewTestCase(
    TaskManagerTestMixin, TaskManagerViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_queue()

    def test_queue_list_view_no_permission(self):
        response = self._request_queue_list()

        self.assertEqual(response.status_code, 403)

    def test_queue_list_view_with_permissions(self):
        self.grant_permission(permission=permission_task_view)

        response = self._request_queue_list()
        self.assertContains(
            response, text=self.test_queue.name, status_code=200
        )
