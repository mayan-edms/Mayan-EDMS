from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings

from documents.models import DocumentType
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from rest_api.tests import BaseAPITestCase
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import Workflow

from .literals import (
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_LABEL_EDITED,
    TEST_WORKFLOW_INITIAL_STATE_COMPLETION, TEST_WORKFLOW_INITIAL_STATE_LABEL,
    TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT, TEST_WORKFLOW_STATE_COMPLETION,
    TEST_WORKFLOW_STATE_LABEL, TEST_WORKFLOW_STATE_LABEL_EDITED,
    TEST_WORKFLOW_TRANSITION_LABEL, TEST_WORKFLOW_TRANSITION_LABEL_EDITED
)


@override_settings(OCR_AUTO_OCR=False)
class WorkflowAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(WorkflowAPITestCase, self).setUp()
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(WorkflowAPITestCase, self).tearDown()

    def _create_workflow(self):
        return Workflow.objects.create(label=TEST_WORKFLOW_LABEL)

    def test_workflow_create_view(self):
        response = self.client.post(
            reverse('rest_api:workflow-list'), {
                'label': TEST_WORKFLOW_LABEL
            }
        )

        workflow = Workflow.objects.first()
        self.assertEqual(Workflow.objects.count(), 1)
        self.assertEqual(response.data['id'], workflow.pk)

    def test_workflow_create_with_document_type_view(self):
        response = self.client.post(
            reverse('rest_api:workflow-list'), {
                'label': TEST_WORKFLOW_LABEL,
                'document_types_pk_list': '{}'.format(self.document_type.pk)
            }
        )

        workflow = Workflow.objects.first()
        self.assertEqual(Workflow.objects.count(), 1)
        self.assertQuerysetEqual(
            workflow.document_types.all(), (repr(self.document_type),)
        )
        self.assertEqual(response.data['id'], workflow.pk)

    def test_workflow_delete_view(self):
        workflow = self._create_workflow()

        self.client.delete(
            reverse('rest_api:workflow-detail', args=(workflow.pk,))
        )

        self.assertEqual(Workflow.objects.count(), 0)

    def test_workflow_detail_view(self):
        workflow = self._create_workflow()

        response = self.client.get(
            reverse('rest_api:workflow-detail', args=(workflow.pk,))
        )

        self.assertEqual(response.data['label'], workflow.label)

    def test_workflow_document_type_create_view(self):
        workflow = self._create_workflow()

        self.client.post(
            reverse(
                'rest_api:workflow-document-type-list',
                args=(workflow.pk,)
            ), data={'document_type_pk': self.document_type.pk}
        )

        self.assertQuerysetEqual(
            workflow.document_types.all(), (repr(self.document_type),)
        )

    def test_workflow_document_type_delete_view(self):
        workflow = self._create_workflow()
        workflow.document_types.add(self.document_type)

        self.client.delete(
            reverse(
                'rest_api:workflow-document-type-detail',
                args=(workflow.pk, self.document_type.pk)
            )
        )

        workflow.refresh_from_db()
        self.assertQuerysetEqual(workflow.document_types.all(), ())
        # The workflow document type entry was deleted and not the document
        # type itself.
        self.assertQuerysetEqual(
            DocumentType.objects.all(), (repr(self.document_type),)
        )

    def test_workflow_document_type_detail_view(self):
        workflow = self._create_workflow()
        workflow.document_types.add(self.document_type)

        response = self.client.get(
            reverse(
                'rest_api:workflow-document-type-detail',
                args=(workflow.pk, self.document_type.pk)
            )
        )

        self.assertEqual(response.data['label'], self.document_type.label)

    def test_workflow_document_type_list_view(self):
        workflow = self._create_workflow()
        workflow.document_types.add(self.document_type)

        response = self.client.get(
            reverse(
                'rest_api:workflow-document-type-list', args=(workflow.pk,)
            )
        )

        self.assertEqual(
            response.data['results'][0]['label'], self.document_type.label
        )

    def test_workflow_list_view(self):
        workflow = self._create_workflow()

        response = self.client.get(reverse('rest_api:workflow-list'))

        self.assertEqual(response.data['results'][0]['label'], workflow.label)

    def test_workflow_put_view(self):
        workflow = self._create_workflow()

        self.client.put(
            reverse('rest_api:workflow-detail', args=(workflow.pk,)),
            data={'label': TEST_WORKFLOW_LABEL_EDITED}
        )

        workflow.refresh_from_db()
        self.assertEqual(workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def test_workflow_patch_view(self):
        workflow = self._create_workflow()

        self.client.patch(
            reverse('rest_api:workflow-detail', args=(workflow.pk,)),
            data={'label': TEST_WORKFLOW_LABEL_EDITED}
        )

        workflow.refresh_from_db()
        self.assertEqual(workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def test_document_type_workflow_list(self):
        workflow = self._create_workflow()
        workflow.document_types.add(self.document_type)

        response = self.client.get(
            reverse(
                'rest_api:documenttype-workflow-list',
                args=(self.document_type.pk,)
            ),
        )

        self.assertEqual(response.data['results'][0]['label'], workflow.label)


@override_settings(OCR_AUTO_OCR=False)
class WorkflowStatesAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(WorkflowStatesAPITestCase, self).setUp()

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(WorkflowStatesAPITestCase, self).tearDown()

    def _create_workflow(self):
        self.workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)

    def _create_workflow_state(self):
        self._create_workflow()
        self.workflow_state = self.workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def test_workflow_state_create_view(self):
        self._create_workflow()

        self.client.post(
            reverse(
                'rest_api:workflowstate-list', args=(self.workflow.pk,)
            ), data={
                'completion': TEST_WORKFLOW_STATE_COMPLETION,
                'label': TEST_WORKFLOW_STATE_LABEL
            }
        )

        self.workflow.refresh_from_db()

        self.assertEqual(
            self.workflow.states.first().label, TEST_WORKFLOW_STATE_LABEL
        )

    def test_workflow_state_delete_view(self):
        self._create_workflow_state()

        self.client.delete(
            reverse(
                'rest_api:workflowstate-detail',
                args=(self.workflow.pk, self.workflow_state.pk)
            ),
        )

        self.workflow.refresh_from_db()

        self.assertEqual(self.workflow.states.count(), 0)

    def test_workflow_state_detail_view(self):
        self._create_workflow_state()

        response = self.client.get(
            reverse(
                'rest_api:workflowstate-detail',
                args=(self.workflow.pk, self.workflow_state.pk)
            ),
        )

        self.assertEqual(
            response.data['label'], TEST_WORKFLOW_STATE_LABEL
        )

    def test_workflow_state_list_view(self):
        self._create_workflow_state()

        response = self.client.get(
            reverse('rest_api:workflowstate-list', args=(self.workflow.pk,)),
        )

        self.assertEqual(
            response.data['results'][0]['label'], TEST_WORKFLOW_STATE_LABEL
        )

    def test_workflow_state_patch_view(self):
        self._create_workflow_state()

        self.client.patch(
            reverse(
                'rest_api:workflowstate-detail',
                args=(self.workflow.pk, self.workflow_state.pk)
            ),
            data={'label': TEST_WORKFLOW_STATE_LABEL_EDITED}
        )

        self.workflow_state.refresh_from_db()

        self.assertEqual(
            self.workflow_state.label,
            TEST_WORKFLOW_STATE_LABEL_EDITED
        )

    def test_workflow_state_put_view(self):
        self._create_workflow_state()

        self.client.put(
            reverse(
                'rest_api:workflowstate-detail',
                args=(self.workflow.pk, self.workflow_state.pk)
            ),
            data={'label': TEST_WORKFLOW_STATE_LABEL_EDITED}
        )

        self.workflow_state.refresh_from_db()

        self.assertEqual(
            self.workflow_state.label,
            TEST_WORKFLOW_STATE_LABEL_EDITED
        )


@override_settings(OCR_AUTO_OCR=False)
class WorkflowTransitionsAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(WorkflowTransitionsAPITestCase, self).setUp()

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(WorkflowTransitionsAPITestCase, self).tearDown()

    def _create_workflow(self):
        self.workflow = Workflow.objects.create(label=TEST_WORKFLOW_LABEL)

    def _create_workflow_states(self):
        self._create_workflow()
        self.workflow_state_1 = self.workflow.states.create(
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
            label=TEST_WORKFLOW_INITIAL_STATE_LABEL
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

    def test_workflow_transition_create_view(self):
        self._create_workflow_states()

        self.client.post(
            reverse(
                'rest_api:workflowtransition-list', args=(self.workflow.pk,)
            ), data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL,
                'origin_state_pk': self.workflow_state_1.pk,
                'destination_state_pk': self.workflow_state_2.pk,
            }
        )

        self.workflow.refresh_from_db()

        self.assertEqual(
            self.workflow.transitions.first().label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_workflow_transition_delete_view(self):
        self._create_workflow_transition()

        self.client.delete(
            reverse(
                'rest_api:workflowtransition-detail',
                args=(self.workflow.pk, self.workflow_transition.pk)
            ),
        )

        self.workflow.refresh_from_db()

        self.assertEqual(self.workflow.transitions.count(), 0)

    def test_workflow_transition_detail_view(self):
        self._create_workflow_transition()

        response = self.client.get(
            reverse(
                'rest_api:workflowtransition-detail',
                args=(self.workflow.pk, self.workflow_transition.pk)
            ),
        )

        self.assertEqual(
            response.data['label'], TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_workflow_transition_list_view(self):
        self._create_workflow_transition()

        response = self.client.get(
            reverse(
                'rest_api:workflowtransition-list', args=(self.workflow.pk,)
            ),
        )

        self.assertEqual(
            response.data['results'][0]['label'],
            TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_workflow_transition_patch_view(self):
        self._create_workflow_transition()

        self.client.patch(
            reverse(
                'rest_api:workflowtransition-detail',
                args=(self.workflow.pk, self.workflow_transition.pk)
            ),
            data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
                'origin_state_pk': self.workflow_state_2.pk,
                'destination_state_pk': self.workflow_state_1.pk,
            }
        )

        self.workflow_transition.refresh_from_db()

        self.assertEqual(
            self.workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )
        self.assertEqual(
            self.workflow_transition.origin_state,
            self.workflow_state_2
        )
        self.assertEqual(
            self.workflow_transition.destination_state,
            self.workflow_state_1
        )

    def test_workflow_transition_put_view(self):
        self._create_workflow_transition()

        self.client.put(
            reverse(
                'rest_api:workflowtransition-detail',
                args=(self.workflow.pk, self.workflow_transition.pk)
            ),
            data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
                'origin_state_pk': self.workflow_state_2.pk,
                'destination_state_pk': self.workflow_state_1.pk,
            }
        )

        self.workflow_transition.refresh_from_db()

        self.assertEqual(
            self.workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )
        self.assertEqual(
            self.workflow_transition.origin_state,
            self.workflow_state_2
        )
        self.assertEqual(
            self.workflow_transition.destination_state,
            self.workflow_state_1
        )


@override_settings(OCR_AUTO_OCR=False)
class DocumentWorkflowsAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(DocumentWorkflowsAPITestCase, self).setUp()

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

    def tearDown(self):
        if hasattr(self, 'document_type'):
            self.document_type.delete()
        super(DocumentWorkflowsAPITestCase, self).tearDown()

    def _create_document(self):
        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object
            )

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

    def _create_workflow_instance_log_entry(self):
        self.document.workflows.first().log_entries.create(
            comment=TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT, transition=self.workflow_transition,
            user=self.admin_user
        )

    def test_workflow_instance_detail_view(self):
        self._create_workflow_transition()
        self._create_document()

        response = self.client.get(
            reverse(
                'rest_api:workflowinstance-detail', args=(
                    self.document.pk, self.document.workflows.first().pk
                )
            ),
        )

        self.assertEqual(
            response.data['workflow']['label'],
            TEST_WORKFLOW_LABEL
        )

    def test_workflow_instance_list_view(self):
        self._create_workflow_transition()
        self._create_document()

        response = self.client.get(
            reverse(
                'rest_api:workflowinstance-list', args=(self.document.pk,)
            ),
        )

        self.assertEqual(
            response.data['results'][0]['workflow']['label'],
            TEST_WORKFLOW_LABEL
        )

    def test_workflow_instance_log_entries_create_view(self):
        self._create_workflow_transition()
        self._create_document()

        workflow_instance = self.document.workflows.first()

        self.client.post(
            reverse(
                'rest_api:workflowinstancelogentry-list', args=(
                    self.document.pk, workflow_instance.pk
                ),
            ), data={'transition_pk': self.workflow_transition.pk}
        )

        workflow_instance.refresh_from_db()

        self.assertEqual(
            workflow_instance.log_entries.first().transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_workflow_instance_log_entries_list_view(self):
        self._create_workflow_transition()
        self._create_document()
        self._create_workflow_instance_log_entry()

        response = self.client.get(
            reverse(
                'rest_api:workflowinstancelogentry-list', args=(
                    self.document.pk, self.document.workflows.first().pk
                )
            ),
        )

        self.assertEqual(
            response.data['results'][0]['transition']['label'],
            TEST_WORKFLOW_TRANSITION_LABEL
        )
