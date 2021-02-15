from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_edited
from ..models import WorkflowTransition
from ..permissions import (
    permission_workflow_edit, permission_workflow_transition,
    permission_workflow_view
)

from .literals import (
    TEST_WORKFLOW_TRANSITION_LABEL, TEST_WORKFLOW_TRANSITION_LABEL_EDITED
)
from .mixins import (
    WorkflowInstanceViewTestMixin, WorkflowTestMixin,
    WorkflowTransitionEventViewTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTransitionViewTestMixin,
    WorkflowViewTestMixin
)


class WorkflowTransitionViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin,
    WorkflowTransitionViewTestMixin, GenericViewTestCase
):
    def test_workflow_transition_create_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self._clear_events()

        response = self._request_test_workflow_transition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowTransition.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_create_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_test_workflow_transition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowTransition.objects.count(), 1)
        self.assertEqual(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].origin_state,
            self.test_workflow_state_1
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].destination_state,
            self.test_workflow_state_2
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_workflow_transition)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow)
        self.assertEqual(events[0].verb, event_workflow_edited.id)

    def test_workflow_transition_delete_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self._clear_events()

        response = self._request_test_workflow_transition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_delete_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_test_workflow_transition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow)
        self.assertEqual(events[0].verb, event_workflow_edited.id)

    def test_workflow_transition_edit_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self._clear_events()

        response = self._request_test_workflow_transition_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_edit_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_test_workflow_transition_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_workflow_transition)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow)
        self.assertEqual(events[0].verb, event_workflow_edited.id)

    def test_workflow_transition_list_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self._clear_events()

        response = self._request_test_workflow_transition_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=404
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_list_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self._clear_events()

        response = self._request_test_workflow_transition_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=200
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowTransitionEventViewTestCase(
    WorkflowInstanceViewTestMixin, WorkflowTestMixin,
    WorkflowTransitionEventViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self._create_test_document_stub()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_workflow_transition_selection_get_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_selection_post_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_event_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_event_list_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_execute_view_no_permission(self):
        """
        Test transitioning a workflow without the transition workflow
        permission.
        """
        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        # Workflow should remain in the same initial state.
        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_execute_view_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_execute_view_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowTransitionFieldViewTestCase(
    WorkflowTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

    def test_workflow_transition_field_create_view_no_permission(self):
        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        self._clear_events()

        response = self._request_workflow_transition_field_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_field_create_view_with_access(self):
        workflow_transition_field_count = self.test_workflow_transition.fields.count()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_workflow_transition_field_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_workflow_transition_field)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow)
        self.assertEqual(events[0].verb, event_workflow_edited.id)

    def test_workflow_transition_field_delete_view_no_permission(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        self._clear_events()

        response = self._request_workflow_transition_field_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_field_delete_view_with_access(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_workflow_transition_field_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow)
        self.assertEqual(events[0].verb, event_workflow_edited.id)

    def test_workflow_transition_field_edit_view_no_permission(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_label = self.test_workflow_transition_field.label

        self._clear_events()

        response = self._request_workflow_transition_field_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_transition_field.refresh_from_db()
        self.assertEqual(
            workflow_transition_field_label,
            self.test_workflow_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_field_edit_view_with_access(self):
        self._create_test_workflow_transition_field()
        workflow_transition_field_label = self.test_workflow_transition_field.label

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_workflow_transition_field_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_transition_field.refresh_from_db()
        self.assertNotEqual(
            workflow_transition_field_label,
            self.test_workflow_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_workflow_transition_field)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow)
        self.assertEqual(events[0].verb, event_workflow_edited.id)

    def test_workflow_transition_field_list_view_no_permission(self):
        self._create_test_workflow_transition_field()

        self._clear_events()

        response = self._request_test_workflow_transition_field_list_view()
        self.assertNotContains(
            response=response,
            text=self.test_workflow_transition_field.label,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_transition_field_list_view_with_access(self):
        self._create_test_workflow_transition_field()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        self._clear_events()

        response = self._request_test_workflow_transition_field_list_view()
        self.assertContains(
            response=response,
            text=self.test_workflow_transition_field.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
