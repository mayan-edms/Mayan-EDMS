from __future__ import unicode_literals

from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests.literals import (
    TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..models import Workflow, WorkflowState, WorkflowTransition
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit
)

from .literals import (
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_INITIAL_STATE_LABEL,
    TEST_WORKFLOW_INITIAL_STATE_COMPLETION, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_COMPLETION, TEST_WORKFLOW_TRANSITION_LABEL
)


class DocumentStateViewTestCase(GenericDocumentViewTestCase):
    def create_workflow(self):
        self.workflow = Workflow.on_organization.create(
            label=TEST_WORKFLOW_LABEL
        )

    def test_workflow_create_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_workflow_create.stored_permission
        )

        response = self.post(
            'document_states:setup_workflow_create', data={
                'label': TEST_WORKFLOW_LABEL,
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(Workflow.on_organization.count(), 1)
        self.assertEquals(
            Workflow.on_organization.all()[0].label, TEST_WORKFLOW_LABEL
        )

    def test_workflow_delete_view_with_permission(self):
        self.create_workflow()

        self.assertEquals(Workflow.on_organization.count(), 1)
        self.assertEquals(
            Workflow.on_organization.all()[0].label, TEST_WORKFLOW_LABEL
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_workflow_delete.stored_permission
        )

        response = self.post(
            'document_states:setup_workflow_delete', args=(self.workflow.pk,),
            follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(Workflow.on_organization.count(), 0)

    def test_workflow_state_create_view_with_permission(self):
        self.create_workflow()

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_workflow_edit.stored_permission
        )

        response = self.post(
            'document_states:setup_workflow_state_create',
            args=(self.workflow.pk,), data={
                'label': TEST_WORKFLOW_STATE_LABEL,
                'completion': TEST_WORKFLOW_STATE_COMPLETION,
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.on_organization.count(), 1)
        self.assertEquals(
            WorkflowState.on_organization.all()[0].label,
            TEST_WORKFLOW_STATE_LABEL
        )
        self.assertEquals(
            WorkflowState.on_organization.all()[0].completion,
            TEST_WORKFLOW_STATE_COMPLETION
        )

    def test_workflow_state_delete_view_with_permission(self):
        self.create_workflow()

        workflow_state = WorkflowState.on_organization.create(
            workflow=self.workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_workflow_edit.stored_permission
        )

        response = self.post(
            'document_states:setup_workflow_state_delete',
            args=(workflow_state.pk,), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.on_organization.count(), 0)
        self.assertEquals(Workflow.on_organization.count(), 1)

    def test_workflow_transition_create_view_with_permission(self):
        self.create_workflow()

        workflow_initial_state = WorkflowState.on_organization.create(
            workflow=self.workflow, label=TEST_WORKFLOW_INITIAL_STATE_LABEL,
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION, initial=True
        )
        workflow_state = WorkflowState.on_organization.create(
            workflow=self.workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_workflow_edit.stored_permission
        )

        response = self.post(
            'document_states:setup_workflow_transition_create',
            args=(self.workflow.pk,), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL,
                'origin_state': workflow_initial_state.pk,
                'destination_state': workflow_state.pk,
            }, follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowTransition.on_organization.count(), 1)
        self.assertEquals(
            WorkflowTransition.on_organization.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEquals(
            WorkflowTransition.on_organization.all()[0].origin_state,
            workflow_initial_state
        )
        self.assertEquals(
            WorkflowTransition.on_organization.all()[0].destination_state,
            workflow_state
        )

    def test_workflow_transition_delete_view_with_permission(self):
        self.create_workflow()

        workflow_initial_state = WorkflowState.on_organization.create(
            workflow=self.workflow, label=TEST_WORKFLOW_INITIAL_STATE_LABEL,
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION, initial=True
        )
        workflow_state = WorkflowState.on_organization.create(
            workflow=self.workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )
        workflow_transition = WorkflowTransition.on_organization.create(
            workflow=self.workflow, label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=workflow_initial_state,
            destination_state=workflow_state
        )

        self.assertEquals(WorkflowTransition.on_organization.count(), 1)

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(
            permission_workflow_edit.stored_permission
        )

        response = self.post(
            'document_states:setup_workflow_transition_delete',
            args=(workflow_transition.pk,), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.on_organization.count(), 2)
        self.assertEquals(Workflow.on_organization.count(), 1)
        self.assertEquals(WorkflowTransition.on_organization.count(), 0)
