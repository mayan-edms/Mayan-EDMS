from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import Workflow, WorkflowState, WorkflowTransition
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_view,
    permission_workflow_tools, permission_workflow_transition
)

from .literals import (
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_LABEL_EDITED, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_COMPLETION, TEST_WORKFLOW_TRANSITION_LABEL,
    TEST_WORKFLOW_TRANSITION_LABEL_EDITED
)
from .mixins import (
    WorkflowStateViewTestMixin, WorkflowTestMixin, WorkflowViewTestMixin,
    WorkflowTransitionViewTestMixin
)


class WorkflowViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, GenericViewTestCase
):
    def test_workflow_create_view_no_permission(self):
        response = self._request_test_workflow_create_view()
        self.assertEquals(response.status_code, 403)

        self.assertEquals(Workflow.objects.count(), 0)

    def test_workflow_create_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_create)

        response = self._request_test_workflow_create_view()
        self.assertEquals(response.status_code, 302)

        self.assertEquals(Workflow.objects.count(), 1)
        self.assertEquals(Workflow.objects.all()[0].label, TEST_WORKFLOW_LABEL)

    def test_workflow_delete_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_delete_view()
        self.assertEquals(response.status_code, 404)

        self.assertTrue(self.test_workflow in Workflow.objects.all())

    def test_workflow_delete_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_delete
        )

        response = self._request_test_workflow_delete_view()
        self.assertEquals(response.status_code, 302)

        self.assertFalse(self.test_workflow in Workflow.objects.all())

    def test_workflow_edit_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_edit_view()
        self.assertEquals(response.status_code, 404)

        self.test_workflow.refresh_from_db()
        self.assertEqual(self.test_workflow.label, TEST_WORKFLOW_LABEL)

    def test_workflow_edit_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_edit_view()
        self.assertEquals(response.status_code, 302)

        self.test_workflow.refresh_from_db()
        self.assertEqual(self.test_workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def test_workflow_list_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_list_view()

        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, text=self.test_workflow.label)

    def test_workflow_list_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, text=self.test_workflow.label)

    def test_workflow_preview_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_preview_view()
        self.assertEquals(response.status_code, 404)

        self.assertTrue(self.test_workflow in Workflow.objects.all())

    def test_workflow_preview_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )
        response = self._request_test_workflow_preview_view()
        self.assertEquals(response.status_code, 200)


class WorkflowStateViewTestCase(
    WorkflowTestMixin, WorkflowStateViewTestMixin, GenericViewTestCase
):
    def test_create_workflow_state_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_state_create_view()
        self.assertEquals(response.status_code, 404)

        self.assertEquals(WorkflowState.objects.count(), 0)

    def test_create_workflow_state_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_create_view()
        self.assertEquals(response.status_code, 302)

        self.assertEquals(WorkflowState.objects.count(), 1)
        self.assertEquals(
            WorkflowState.objects.all()[0].label, TEST_WORKFLOW_STATE_LABEL
        )
        self.assertEquals(
            WorkflowState.objects.all()[0].completion,
            TEST_WORKFLOW_STATE_COMPLETION
        )

    def test_create_workflow_state_invalid_completion_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_create_view(
            extra_data={'completion': ''}
        )
        self.assertEquals(response.status_code, 302)

        self.assertEquals(WorkflowState.objects.count(), 1)
        self.assertEquals(
            WorkflowState.objects.all()[0].label, TEST_WORKFLOW_STATE_LABEL
        )
        self.assertEquals(
            WorkflowState.objects.all()[0].completion, 0
        )

    def test_delete_workflow_state_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        response = self._request_test_workflow_state_delete_view()
        self.assertEquals(response.status_code, 404)

        self.assertEquals(WorkflowState.objects.count(), 2)

    def test_delete_workflow_state_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_delete_view()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(WorkflowState.objects.count(), 1)

    def test_edit_workflow_state_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        workflow_state_label = self.test_workflow_state_1.label

        response = self._request_test_workflow_state_edit_view()
        self.assertEquals(response.status_code, 404)

        self.test_workflow_state_1.refresh_from_db()
        self.assertEquals(
            self.test_workflow_state_1.label, workflow_state_label
        )

    def test_edit_workflow_state_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        workflow_state_label = self.test_workflow_state_1.label

        response = self._request_test_workflow_state_edit_view()
        self.assertEquals(response.status_code, 302)

        self.test_workflow_state_1.refresh_from_db()
        self.assertNotEquals(
            self.test_workflow_state_1.label, workflow_state_label
        )

    def test_workflow_state_list_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        response = self._request_test_workflow_state_list_view()
        self.assertEquals(response.status_code, 404)

    def test_workflow_state_list_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_state_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, text=self.test_workflow_state_1.label)


class WorkflowToolViewTestCase(WorkflowTestMixin, GenericDocumentViewTestCase):
    def _request_workflow_launch_view(self):
        return self.post(
            viewname='document_states:tool_launch_all_workflows',
        )

    def test_tool_launch_all_workflows_view_no_permission(self):
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.assertEqual(self.test_document.workflows.count(), 0)

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.test_document.workflows.count(), 0)

    def test_tool_launch_all_workflows_view_with_permission(self):
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_permission(permission=permission_workflow_tools)
        self.assertEqual(self.test_document.workflows.count(), 0)

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.first().workflow, self.test_workflow
        )


class WorkflowTransitionViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_document = False

    def test_create_test_workflow_transition_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        response = self._request_test_workflow_transition_create_view()
        self.assertEquals(response.status_code, 404)

        self.assertEquals(WorkflowTransition.objects.count(), 0)

    def test_create_test_workflow_transition_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_create_view()
        self.assertEquals(response.status_code, 302)

        self.assertEquals(WorkflowTransition.objects.count(), 1)
        self.assertEquals(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEquals(
            WorkflowTransition.objects.all()[0].origin_state,
            self.test_workflow_state_1
        )
        self.assertEquals(
            WorkflowTransition.objects.all()[0].destination_state,
            self.test_workflow_state_2
        )

    def test_delete_workflow_transition_no_permissions(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_delete_view()
        self.assertEquals(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )

    def test_delete_workflow_transition_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(permission=permission_workflow_edit, obj=self.test_workflow)

        response = self._request_test_workflow_transition_delete_view()
        self.assertEquals(response.status_code, 302)

        self.assertFalse(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )

    def test_edit_workflow_transition_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_edit_view()
        self.assertEquals(response.status_code, 404)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label, TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_edit_workflow_transition_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_edit_view()
        self.assertEquals(response.status_code, 302)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )

    def test_workflow_transition_list_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=404
        )

    def test_workflow_transition_list_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_transition_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=200
        )

    def test_transition_workflow_no_access(self):
        """
        Test transitioning a workflow without the transition workflow
        permission.
        """
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self.upload_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        response = self._request_test_workflow_transition()
        self.assertEqual(response.status_code, 200)

        # Workflow should remain in the same initial state
        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_transition_workflow_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self.upload_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        self.grant_permission(permission=permission_workflow_transition)

        response = self._request_test_workflow_transition()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

    def test_transition_workflow_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self.upload_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        self.grant_permission(permission=permission_workflow_transition)

        response = self._request_test_workflow_transition()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )


class WorkflowTransitionEventViewTestCase(
    WorkflowTestMixin, GenericDocumentViewTestCase
):
    def _request_test_workflow_transition_event_list_view(self):
        return self.get(
            viewname='document_states:setup_workflow_transition_events',
            kwargs={'pk': self.test_workflow_transition.pk}
        )

    def test_workflow_transition_event_list_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEquals(response.status_code, 404)

    def test_workflow_transition_event_list_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEquals(response.status_code, 200)
