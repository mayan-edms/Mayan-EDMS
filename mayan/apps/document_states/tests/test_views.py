from __future__ import unicode_literals

from common.tests import GenericViewTestCase
from documents.tests import (
    GenericDocumentViewTestCase, TEST_SMALL_DOCUMENT_PATH
)

from ..models import Workflow, WorkflowState, WorkflowTransition
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_view,
    permission_workflow_tools, permission_workflow_transition
)

from .literals import (
    TEST_WORKFLOW_INITIAL_STATE_LABEL, TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
    TEST_WORKFLOW_INTERNAL_NAME, TEST_WORKFLOW_LABEL,
    TEST_WORKFLOW_LABEL_EDITED, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_LABEL_EDITED, TEST_WORKFLOW_STATE_COMPLETION,
    TEST_WORKFLOW_TRANSITION_LABEL, TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
)
from .mixins import WorkflowTestMixin


class DocumentStateViewTestCase(WorkflowTestMixin, GenericViewTestCase):
    def setUp(self):
        super(DocumentStateViewTestCase, self).setUp()
        self.login_user()

    def _request_workflow_create_view(self):
        return self.post(
            viewname='document_states:setup_workflow_create', data={
                'label': TEST_WORKFLOW_LABEL,
                'internal_name': TEST_WORKFLOW_INTERNAL_NAME,
            }
        )

    def test_workflow_create_view_no_permission(self):
        response = self._request_workflow_create_view()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Workflow.objects.count(), 0)

    def test_workflow_create_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_create)
        response = self._request_workflow_create_view()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Workflow.objects.count(), 1)
        self.assertEquals(Workflow.objects.all()[0].label, TEST_WORKFLOW_LABEL)

    def _request_workflow_delete_view(self):
        return self.post(
            viewname='document_states:setup_workflow_delete', args=(
                self.workflow.pk,
            ),
        )

    def test_workflow_delete_view_no_access(self):
        self._create_workflow()
        response = self._request_workflow_delete_view()
        self.assertEquals(response.status_code, 403)
        self.assertTrue(self.workflow in Workflow.objects.all())

    def test_workflow_delete_view_with_access(self):
        self._create_workflow()
        self.grant_access(permission=permission_workflow_delete, obj=self.workflow)
        response = self._request_workflow_delete_view()
        self.assertEquals(response.status_code, 302)
        self.assertFalse(self.workflow in Workflow.objects.all())

    def _request_workflow_edit_view(self):
        return self.post(
            viewname='document_states:setup_workflow_edit', args=(
                self.workflow.pk,
            ), data={
                'label': TEST_WORKFLOW_LABEL_EDITED,
                'internal_name': self.workflow.internal_name
            }
        )

    def test_workflow_edit_view_no_access(self):
        self._create_workflow()
        response = self._request_workflow_edit_view()
        self.assertEquals(response.status_code, 403)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.label, TEST_WORKFLOW_LABEL)

    def test_workflow_edit_view_with_access(self):
        self._create_workflow()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_edit_view()
        self.assertEquals(response.status_code, 302)
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def _request_workflow_list_view(self):
        return self.get(
            viewname='document_states:setup_workflow_list',
        )

    def test_workflow_list_view_no_access(self):
        self._create_workflow()
        response = self._request_workflow_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, text=self.workflow.label)

    def test_workflow_list_view_with_access(self):
        self._create_workflow()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, text=self.workflow.label)

    def _request_workflow_preview_view(self):
        return self.get(
            viewname='document_states:workflow_preview', args=(
                self.workflow.pk,
            ),
        )

    def test_workflow_preview_view_no_access(self):
        self._create_workflow()
        response = self._request_workflow_preview_view()
        self.assertEquals(response.status_code, 403)
        self.assertTrue(self.workflow in Workflow.objects.all())

    def test_workflow_preview_view_with_access(self):
        self._create_workflow()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_preview_view()
        self.assertEquals(response.status_code, 200)


class DocumentStateStateViewTestCase(WorkflowTestMixin, GenericViewTestCase):
    def setUp(self):
        super(DocumentStateStateViewTestCase, self).setUp()
        self.login_user()

    def _request_workflow_state_create_view(self, extra_data=None):
        data = {
            'label': TEST_WORKFLOW_STATE_LABEL,
            'completion': TEST_WORKFLOW_STATE_COMPLETION,
        }
        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='document_states:setup_workflow_state_create',
            args=(self.workflow.pk,), data=data
        )

    def test_create_workflow_state_no_access(self):
        self._create_workflow()
        response = self._request_workflow_state_create_view()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(WorkflowState.objects.count(), 0)

    def test_create_workflow_state_with_access(self):
        self._create_workflow()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_create_view()
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
        self._create_workflow()

        self.grant_access(obj=self.workflow, permission=permission_workflow_edit)

        response = self._request_workflow_state_create_view(
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

    def _request_workflow_state_delete_view(self):
        return self.post(
            viewname='document_states:setup_workflow_state_delete',
            args=(self.workflow_state.pk,)
        )

    def test_delete_workflow_state_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        response = self._request_workflow_state_delete_view()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(WorkflowState.objects.count(), 2)

    def test_delete_workflow_state_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_delete_view()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(WorkflowState.objects.count(), 1)

    def _request_workflow_state_edit_view(self):
        return self.post(
            viewname='document_states:setup_workflow_state_edit',
            args=(self.workflow_state.pk,), data={
                'label': TEST_WORKFLOW_STATE_LABEL_EDITED
            }
        )

    def test_edit_workflow_state_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        response = self._request_workflow_state_edit_view()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(self.workflow_state.label, TEST_WORKFLOW_STATE_LABEL)

    def test_edit_workflow_state_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_state_edit_view()
        self.assertEquals(response.status_code, 302)
        self.workflow_state.refresh_from_db()
        self.assertEquals(self.workflow_state.label, TEST_WORKFLOW_STATE_LABEL_EDITED)

    def _request_workflow_state_list_view(self):
        return self.get(
            viewname='document_states:setup_workflow_state_list',
            args=(self.workflow.pk,)
        )

    def test_workflow_state_list_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        response = self._request_workflow_state_list_view()
        self.assertEquals(response.status_code, 403)

    def test_workflow_state_list_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_state_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, text=self.workflow_state.label)


class DocumentStateToolViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentStateToolViewTestCase, self).setUp()
        self.login_user()

    def _create_workflow(self):
        self.workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)
        self.workflow.document_types.add(self.document_type)

    def _create_workflow_states(self):
        self._create_workflow()
        self.workflow_state_1 = self.workflow.states.create(
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
            initial=True, label=TEST_WORKFLOW_INITIAL_STATE_LABEL
        )
        self.workflow_state_2 = self.workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _create_workflow_transition(self):
        self._create_workflow_states()
        self.workflow_transition = self.workflow.transitions.create(
            label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.workflow_state_1,
            destination_state=self.workflow_state_2,
        )

    def _request_workflow_launch_view(self):
        return self.post(
            'document_states:tool_launch_all_workflows',
        )

    def test_tool_launch_all_workflows_view_no_permission(self):
        self._create_workflow_transition()
        self.assertEqual(self.document.workflows.count(), 0)
        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document.workflows.count(), 0)

    def test_tool_launch_all_workflows_view_with_permission(self):
        self._create_workflow_transition()
        self.grant_permission(permission=permission_workflow_tools)
        self.assertEqual(self.document.workflows.count(), 0)
        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.document.workflows.first().workflow, self.workflow
        )


class DocumentStateTransitionViewTestCase(WorkflowTestMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentStateTransitionViewTestCase, self).setUp()
        self.login_user()

    def _create_document(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document_2 = self.document_type.new_document(
                file_object=file_object
            )

    def _request_workflow_transition_create_view(self):
        return self.post(
            viewname='document_states:setup_workflow_transition_create',
            args=(self.workflow.pk,), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL,
                'origin_state': self.workflow_initial_state.pk,
                'destination_state': self.workflow_state.pk,
            }
        )

    def test_create_workflow_transition_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        response = self._request_workflow_transition_create_view()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(WorkflowTransition.objects.count(), 0)

    def test_create_workflow_transition_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_create_view()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(WorkflowTransition.objects.count(), 1)
        self.assertEquals(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEquals(
            WorkflowTransition.objects.all()[0].origin_state,
            self.workflow_initial_state
        )
        self.assertEquals(
            WorkflowTransition.objects.all()[0].destination_state,
            self.workflow_state
        )

    def _request_workflow_transition_delete_view(self):
        return self.post(
            viewname='document_states:setup_workflow_transition_delete',
            args=(self.workflow_transition.pk,)
        )

    def test_delete_workflow_transition_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        response = self._request_workflow_transition_delete_view()
        self.assertEquals(response.status_code, 403)
        self.assertTrue(self.workflow_transition in WorkflowTransition.objects.all())

    def test_delete_workflow_transition_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_delete_view()
        self.assertEquals(response.status_code, 302)
        self.assertFalse(self.workflow_transition in WorkflowTransition.objects.all())

    def _request_workflow_transition_edit_view(self):
        return self.post(
            viewname='document_states:setup_workflow_transition_edit',
            args=(self.workflow_transition.pk,), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
                'origin_state': self.workflow_initial_state.pk,
                'destination_state': self.workflow_state.pk,
            }
        )

    def test_edit_workflow_transition_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        response = self._request_workflow_transition_edit_view()
        self.assertEquals(response.status_code, 403)
        self.workflow_transition.refresh_from_db()
        self.assertEqual(
            self.workflow_transition.label, TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_edit_workflow_transition_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_edit_view()
        self.assertEquals(response.status_code, 302)
        self.workflow_transition.refresh_from_db()
        self.assertEqual(
            self.workflow_transition.label, TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )

    def _request_workflow_transition_list_view(self):
        return self.get(
            viewname='document_states:setup_workflow_transition_list',
            args=(self.workflow.pk,)
        )

    def test_workflow_transition_list_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        response = self._request_workflow_transition_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertNotContains(response, text=self.workflow_transition.label)

    def test_workflow_transition_list_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_view, obj=self.workflow)
        response = self._request_workflow_transition_list_view()
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, text=self.workflow_transition.label)

    def _request_workflow_transition(self):
        return self.post(
            viewname='document_states:workflow_instance_transition',
            args=(self.workflow_instance.pk,), data={
                'transition': self.workflow_transition.pk,
            }
        )

    def test_transition_workflow_no_access(self):
        """
        Test transitioning a workflow without the transition workflow
        permission.
        """
        self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self._create_workflow_states()
        self._create_workflow_transitions()
        self._create_document()
        self.workflow_instance = self.document_2.workflows.first()
        response = self._request_workflow_transition()
        self.assertEqual(response.status_code, 200)
        # Workflow should remain in the same initial state
        self.assertEqual(
            self.workflow_instance.get_current_state(), self.workflow_initial_state
        )

    def test_transition_workflow_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self._create_workflow_states()
        self._create_workflow_transitions()
        self._create_document()
        self.workflow_instance = self.document_2.workflows.first()
        self.grant_permission(permission=permission_workflow_transition)
        response = self._request_workflow_transition()
        self.assertEqual(response.status_code, 302)
        # Workflow should remain in the same initial state
        self.assertEqual(
            self.workflow_instance.get_current_state(), self.workflow_state
        )

    def test_transition_workflow_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self._create_workflow()
        self.workflow.document_types.add(self.document_type)
        self._create_workflow_states()
        self._create_workflow_transitions()
        self._create_document()
        self.workflow_instance = self.document_2.workflows.first()
        self.grant_permission(permission=permission_workflow_transition)
        response = self._request_workflow_transition()
        self.assertEqual(response.status_code, 302)
        # Workflow should remain in the same initial state
        self.assertEqual(
            self.workflow_instance.get_current_state(), self.workflow_state
        )


class DocumentStateTransitionEventViewTestCase(WorkflowTestMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentStateTransitionEventViewTestCase, self).setUp()
        self.login_user()

    def _request_workflow_transition_event_list_view(self):
        return self.get(
            viewname='document_states:setup_workflow_transition_events',
            args=(self.workflow_transition.pk,)
        )

    def test_workflow_transition_event_list_no_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        response = self._request_workflow_transition_event_list_view()
        self.assertEquals(response.status_code, 403)

    def test_workflow_transition_event_list_with_access(self):
        self._create_workflow()
        self._create_workflow_states()
        self._create_workflow_transition()
        self.grant_access(permission=permission_workflow_edit, obj=self.workflow)
        response = self._request_workflow_transition_event_list_view()
        self.assertEquals(response.status_code, 200)
