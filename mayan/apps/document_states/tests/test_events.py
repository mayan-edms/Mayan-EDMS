from actstream.models import Action

from mayan.apps.common.tests.base import GenericViewTestCase

from ..events import event_workflow_created, event_workflow_edited
from ..models import Workflow
from ..permissions import permission_workflow_create, permission_workflow_edit

from .mixins import WorkflowTestMixin, WorkflowViewTestMixin


class WorkflowEventsTestCase(WorkflowTestMixin, WorkflowViewTestMixin, GenericViewTestCase):
    def test_workflow_create_event_no_permissions(self):
        action_count = Action.objects.count()

        response = self._request_test_workflow_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Action.objects.count(), action_count)

    def test_workflow_create_event_with_permissions(self):
        self.grant_permission(permission=permission_workflow_create)

        action_count = Action.objects.count()

        response = self._request_test_workflow_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        workflow = Workflow.objects.first()

        self.assertEqual(event.verb, event_workflow_created.id)
        self.assertEqual(event.target, workflow)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_edit_event_no_permissions(self):
        self._create_test_workflow()

        action_count = Action.objects.count()

        response = self._request_test_workflow_edit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Action.objects.count(), action_count)

    def test_workflow_edit_event_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        action_count = Action.objects.count()

        response = self._request_test_workflow_edit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.target, self.test_workflow)
        self.assertEqual(event.actor, self._test_case_user)
