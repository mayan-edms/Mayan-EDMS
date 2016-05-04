from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings

from rest_framework.test import APITestCase

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from ..models import Folder

from .literals import TEST_FOLDER_EDITED_LABEL, TEST_FOLDER_LABEL


class FolderAPITestCase(APITestCase):
    """
    Test the folder API endpoints
    """

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

    def test_folder_create(self):
        response = self.client.post(
            reverse('rest_api:folder-list'), {'label': TEST_FOLDER_LABEL}
        )

        folder = Folder.objects.first()

        self.assertEqual(response.data['id'], folder.pk)
        self.assertEqual(response.data['label'], TEST_FOLDER_LABEL)

        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(folder.label, TEST_FOLDER_LABEL)

    def test_folder_delete(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.client.delete(
            reverse('rest_api:folder-detail', args=(folder.pk,))
        )

        self.assertEqual(Folder.objects.count(), 0)

    def test_folder_edit(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        self.client.put(
            reverse('rest_api:folder-detail', args=(folder.pk,)),
            {'label': TEST_FOLDER_EDITED_LABEL}
        )

        folder = Folder.objects.first()

        self.assertEqual(folder.label, TEST_FOLDER_EDITED_LABEL)

    @override_settings(OCR_AUTO_OCR=False)
    def test_folder_add_document(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=file_object,
            )

        self.client.post(
            reverse('rest_api:folder-document-list', args=(folder.pk,)),
            {'document': document.pk}
        )

        self.assertEqual(folder.documents.count(), 1)

    @override_settings(OCR_AUTO_OCR=False)
    def test_folder_remove_document(self):
        folder = Folder.objects.create(label=TEST_FOLDER_LABEL)

        document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            document = document_type.new_document(
                file_object=file_object,
            )

        folder.documents.add(document)

        self.client.delete(
            reverse('rest_api:folder-document', args=(folder.pk, document.pk)),
        )

        self.assertEqual(folder.documents.count(), 0)
