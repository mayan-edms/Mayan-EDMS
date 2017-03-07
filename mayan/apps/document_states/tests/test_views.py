from __future__ import unicode_literals

from common.tests.test_views import GenericViewTestCase
from documents.tests.test_views import GenericDocumentViewTestCase

from ..models import Workflow, WorkflowState, WorkflowTransition
from ..permissions import permission_workflow_tools

from .literals import (
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_INITIAL_STATE_LABEL,
    TEST_WORKFLOW_INITIAL_STATE_COMPLETION, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_COMPLETION, TEST_WORKFLOW_TRANSITION_LABEL
)


class DocumentStateViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(DocumentStateViewTestCase, self).setUp()

        self.login_admin_user()

    def test_creating_workflow(self):
        response = self.post(
            'document_states:setup_workflow_create',
            data={
                'label': TEST_WORKFLOW_LABEL,
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(Workflow.objects.count(), 1)
        self.assertEquals(Workflow.objects.all()[0].label, TEST_WORKFLOW_LABEL)

    def test_delete_workflow(self):
        workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)

        self.assertEquals(Workflow.objects.count(), 1)
        self.assertEquals(Workflow.objects.all()[0].label, TEST_WORKFLOW_LABEL)

        response = self.post(
            'document_states:setup_workflow_delete', args=(workflow.pk,),
            follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(Workflow.objects.count(), 0)

    def test_create_workflow_state(self):
        workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)

        response = self.post(
            'document_states:setup_workflow_state_create',
            args=(workflow.pk,),
            data={
                'label': TEST_WORKFLOW_STATE_LABEL,
                'completion': TEST_WORKFLOW_STATE_COMPLETION,
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.objects.count(), 1)
        self.assertEquals(
            WorkflowState.objects.all()[0].label, TEST_WORKFLOW_STATE_LABEL
        )
        self.assertEquals(
            WorkflowState.objects.all()[0].completion,
            TEST_WORKFLOW_STATE_COMPLETION
        )

    def test_delete_workflow_state(self):
        workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)
        workflow_state = WorkflowState.objects.create(
            workflow=workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )

        response = self.post(
            'document_states:setup_workflow_state_delete',
            args=(workflow_state.pk,), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.objects.count(), 0)
        self.assertEquals(Workflow.objects.count(), 1)

    def test_create_workflow_transition(self):
        workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)
        workflow_initial_state = WorkflowState.objects.create(
            workflow=workflow, label=TEST_WORKFLOW_INITIAL_STATE_LABEL,
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION, initial=True
        )
        workflow_state = WorkflowState.objects.create(
            workflow=workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )

        response = self.post(
            'document_states:setup_workflow_transition_create',
            args=(workflow.pk,), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL,
                'origin_state': workflow_initial_state.pk,
                'destination_state': workflow_state.pk,
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowTransition.objects.count(), 1)
        self.assertEquals(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEquals(
            WorkflowTransition.objects.all()[0].origin_state,
            workflow_initial_state
        )
        self.assertEquals(
            WorkflowTransition.objects.all()[0].destination_state,
            workflow_state
        )

    def test_delete_workflow_transition(self):
        workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)
        workflow_initial_state = WorkflowState.objects.create(
            workflow=workflow, label=TEST_WORKFLOW_INITIAL_STATE_LABEL,
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION, initial=True
        )
        workflow_state = WorkflowState.objects.create(
            workflow=workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )
        workflow_transition = WorkflowTransition.objects.create(
            workflow=workflow, label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=workflow_initial_state,
            destination_state=workflow_state
        )

        self.assertEquals(WorkflowTransition.objects.count(), 1)

        response = self.post(
            'document_states:setup_workflow_transition_delete',
            args=(workflow_transition.pk,), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.objects.count(), 2)
        self.assertEquals(Workflow.objects.count(), 1)
        self.assertEquals(WorkflowTransition.objects.count(), 0)


class DocumentStateToolViewTestCase(GenericDocumentViewTestCase):
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

    def test_tool_launch_all_workflows_view_no_permission(self):
        self._create_workflow_transition()

        self.login_user()

        self.assertEqual(self.document.workflows.count(), 0)

        response = self.post(
            'document_states:tool_launch_all_workflows',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.document.workflows.count(), 0)

    def test_tool_launch_all_workflows_view_with_permission(self):
        self._create_workflow_transition()

        self.login_user()
        self.grant(permission_workflow_tools)

        self.assertEqual(self.document.workflows.count(), 0)

        response = self.post(
            'document_states:tool_launch_all_workflows',
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.document.workflows.first().workflow, self.workflow
        )
