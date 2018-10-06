from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils.encoding import force_text

from rest_framework import status
from rest_framework.test import APITestCase

from documents.tests import DocumentTestMixin
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import Cabinet

from .literals import TEST_CABINET_EDITED_LABEL, TEST_CABINET_LABEL


@override_settings(OCR_AUTO_OCR=False)
class CabinetAPITestCase(DocumentTestMixin, APITestCase):
    """
    Test the cabinet API endpoints
    """
    auto_upload_document = False

    def setUp(self):
        super(CabinetAPITestCase, self).setUp()

        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

        self.document = self.upload_document()
        self.document_2 = self.upload_document()

    def test_cabinet_create(self):
        response = self.client.post(
            reverse('rest_api:cabinet-list'), {'label': TEST_CABINET_LABEL}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertEqual(Cabinet.objects.count(), 1)
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_create_with_single_document(self):
        response = self.client.post(
            reverse('rest_api:cabinet-list'), {
                'label': TEST_CABINET_LABEL, 'documents_pk_list': '{}'.format(
                    self.document.pk
                )
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.document),)
        )
        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

    def test_cabinet_create_with_multiple_documents(self):
        response = self.client.post(
            reverse('rest_api:cabinet-list'), {
                'label': TEST_CABINET_LABEL,
                'documents_pk_list': '{},{}'.format(
                    self.document.pk, self.document_2.pk
                )
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cabinet = Cabinet.objects.first()

        self.assertEqual(response.data['id'], cabinet.pk)
        self.assertEqual(response.data['label'], TEST_CABINET_LABEL)

        self.assertEqual(Cabinet.objects.count(), 1)

        self.assertEqual(cabinet.label, TEST_CABINET_LABEL)

        self.assertQuerysetEqual(
            cabinet.documents.all(), map(
                repr, (self.document, self.document_2)
            )
        )

    def test_cabinet_document_delete(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
        cabinet.documents.add(self.document)

        response = self.client.delete(
            reverse(
                'rest_api:cabinet-document',
                args=(cabinet.pk, self.document.pk)
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(cabinet.documents.count(), 0)

    def test_cabinet_document_detail(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
        cabinet.documents.add(self.document)

        response = self.client.get(
            reverse(
                'rest_api:cabinet-document',
                args=(cabinet.pk, self.document.pk)
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['uuid'], force_text(self.document.uuid)
        )

    def test_cabinet_document_list(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
        cabinet.documents.add(self.document)

        response = self.client.get(
            reverse('rest_api:cabinet-document-list', args=(cabinet.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['uuid'], force_text(self.document.uuid)
        )

    def test_cabinet_delete(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self.client.delete(
            reverse('rest_api:cabinet-detail', args=(cabinet.pk,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Cabinet.objects.count(), 0)

    def test_cabinet_edit_via_patch(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self.client.patch(
            reverse('rest_api:cabinet-detail', args=(cabinet.pk,)),
            {'label': TEST_CABINET_EDITED_LABEL}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cabinet.refresh_from_db()

        self.assertEqual(cabinet.label, TEST_CABINET_EDITED_LABEL)

    def test_cabinet_edit_via_put(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self.client.put(
            reverse('rest_api:cabinet-detail', args=(cabinet.pk,)),
            {'label': TEST_CABINET_EDITED_LABEL}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cabinet.refresh_from_db()

        self.assertEqual(cabinet.label, TEST_CABINET_EDITED_LABEL)

    def test_cabinet_add_document(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self.client.post(
            reverse('rest_api:cabinet-document-list', args=(cabinet.pk,)), {
                'documents_pk_list': '{}'.format(self.document.pk)
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertQuerysetEqual(
            cabinet.documents.all(), (repr(self.document),)
        )

    def test_cabinet_add_multiple_documents(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        response = self.client.post(
            reverse('rest_api:cabinet-document-list', args=(cabinet.pk,)), {
                'documents_pk_list': '{},{}'.format(
                    self.document.pk, self.document_2.pk
                )
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertQuerysetEqual(
            cabinet.documents.all(), map(
                repr, (self.document, self.document_2)
            )
        )

    def test_cabinet_list_view(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)
        Cabinet.objects.create(
            label=TEST_CABINET_LABEL, parent=cabinet
        )

        response = self.client.get(
            reverse('rest_api:cabinet-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], cabinet.label)

    def test_cabinet_remove_document(self):
        cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

        cabinet.documents.add(self.document)

        response = self.client.delete(
            reverse(
                'rest_api:cabinet-document', args=(
                    cabinet.pk, self.document.pk
                )
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cabinet.documents.count(), 0)
