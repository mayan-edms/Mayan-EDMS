from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.utils.encoding import force_text

from rest_framework.test import APITestCase

from documents.models import DocumentType
from documents.permissions import permission_document_type_view
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import Workflow

from .literals import TEST_WORKFLOW_LABEL, TEST_WORKFLOW_LABEL_EDITED


@override_settings(OCR_AUTO_OCR=False)
class WorkflowAPITestCase(APITestCase):
    def setUp(self):
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

        response = self.client.post(
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

        response = self.client.delete(
            reverse(
                'rest_api:workflow-document-type-detail',
                args=(workflow.pk, self.document_type.pk)
            )
        )

        workflow.refresh_from_db()
        self.assertQuerysetEqual(workflow.document_types.all(), ())

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
            reverse('rest_api:workflow-document-type-list',
            args=(workflow.pk,))
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

        response = self.client.put(
            reverse('rest_api:workflow-detail', args=(workflow.pk,)),
            data={'label': TEST_WORKFLOW_LABEL_EDITED}
        )

        workflow.refresh_from_db()
        self.assertEqual(workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def test_workflow_patch_view(self):
        workflow = self._create_workflow()

        response = self.client.patch(
            reverse('rest_api:workflow-detail', args=(workflow.pk,)),
            data={'label': TEST_WORKFLOW_LABEL_EDITED}
        )

        workflow.refresh_from_db()
        self.assertEqual(workflow.label, TEST_WORKFLOW_LABEL_EDITED)
