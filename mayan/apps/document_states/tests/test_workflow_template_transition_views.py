from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_template_edited
from ..models import WorkflowTransition
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .literals import TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
from .mixins.workflow_template_mixins import (
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin
)
from .mixins.workflow_template_transition_mixins import (
    WorkflowTemplateTransitionViewTestMixin
)


class WorkflowTransitionViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin,
    WorkflowTemplateTransitionViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()

    def test_workflow_template_transition_create_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_transition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowTransition.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_create_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowTransition.objects.count(), 1)
        self.assertEqual(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].origin_state,
            self._test_workflow_template_states[0]
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].destination_state,
            self._test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_delete_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_workflow_template_transition in WorkflowTransition.objects.all()
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_delete_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self._test_workflow_template_transition in WorkflowTransition.objects.all()
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_edit_view_no_permission(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self._test_workflow_template_transition.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_view_with_access(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self._test_workflow_template_transition.label

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_list_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_view()
        self.assertNotContains(
            response=response,
            text=self._test_workflow_template_transition.label,
            status_code=404
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_list_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_view()
        self.assertContains(
            response=response,
            text=self._test_workflow_template_transition.label,
            status_code=200
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
