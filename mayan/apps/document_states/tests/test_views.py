from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from documents.models import DocumentType
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL
)

from ..models import Workflow, WorkflowState, WorkflowTransition

from .literals import (
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_INITIAL_STATE_LABEL,
    TEST_WORKFLOW_INITIAL_STATE_COMPLETION, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_COMPLETION, TEST_WORKFLOW_TRANSITION_LABEL
)


class DocumentStateViewTestCase(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()
        # Login the admin user
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        self.assertTrue(self.admin_user.is_authenticated())

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        self.document_type.delete()

    def test_creating_workflow(self):
        response = self.client.post(
            reverse(
                'document_states:setup_workflow_create'
            ), data={
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

        response = self.client.post(
            reverse(
                'document_states:setup_workflow_delete', args=(workflow.pk,)
            ), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(Workflow.objects.count(), 0)

    def test_create_workflow_state(self):
        workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)

        response = self.client.post(
            reverse(
                'document_states:setup_workflow_state_create',
                args=(workflow.pk,)
            ), data={
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

        response = self.client.post(
            reverse(
                'document_states:setup_workflow_state_delete',
                args=(workflow_state.pk,)
            ), follow=True
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

        response = self.client.post(
            reverse(
                'document_states:setup_workflow_transition_create',
                args=(workflow.pk,)
            ), data={
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

        response = self.client.post(
            reverse(
                'document_states:setup_workflow_transition_delete',
                args=(workflow_transition.pk,)
            ), follow=True
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(WorkflowState.objects.count(), 2)
        self.assertEquals(Workflow.objects.count(), 1)
        self.assertEquals(WorkflowTransition.objects.count(), 0)
