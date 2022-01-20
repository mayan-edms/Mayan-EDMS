from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import (
    WorkflowTransitionFieldTestMixin, WorkflowTransitionFieldViewTestMixin,
    WorkflowTemplateTransitionViewTestMixin
)


class WorkflowTransitionFieldViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTemplateTransitionViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_template_transition_field_create_view_no_permission(self):
        workflow_template_transition_field_count = self._test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_workflow_template_transition_field_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_create_view_with_access(self):
        workflow_template_transition_field_count = self._test_workflow_template_transition.fields.count()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_workflow_template_transition_field_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_transition_field
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_delete_view_no_permission(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_count = self._test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_workflow_template_transition_field_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_delete_view_with_access(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_count = self._test_workflow_template_transition.fields.count()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_workflow_template_transition_field_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_edit_view_no_permission(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_label = self._test_workflow_template_transition_field.label

        self._clear_events()

        response = self._request_workflow_template_transition_field_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_workflow_template_transition_field.refresh_from_db()
        self.assertEqual(
            workflow_template_transition_field_label,
            self._test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_edit_view_with_access(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_label = self._test_workflow_template_transition_field.label

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_workflow_template_transition_field_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_workflow_template_transition_field.refresh_from_db()
        self.assertNotEqual(
            workflow_template_transition_field_label,
            self._test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_transition_field
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_list_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_view()
        self.assertNotContains(
            response=response,
            text=self._test_workflow_template_transition_field.label,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_list_view_with_access(self):
        self._create_test_workflow_template_transition_field()
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_view()
        self.assertContains(
            response=response,
            text=self._test_workflow_template_transition_field.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
