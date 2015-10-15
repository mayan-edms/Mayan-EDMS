from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from documents.models import DocumentType
from documents.tests.literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)

from ..models import MetadataType, DocumentMetadata

from .literals import (
    TEST_DOCUMENT_TYPE_2, TEST_DOCUMENT_METADATA_VALUE_2,
    TEST_METADATA_TYPE_LABEL, TEST_METADATA_TYPE_LABEL_2,
    TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_NAME_2
)


class DocumentMetadataTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
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

        self.metadata_type = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME, label=TEST_METADATA_TYPE_LABEL
        )

        self.document_type.metadata.create(metadata_type=self.metadata_type)

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document_type.delete()
        self.admin_user.delete()
        self.metadata_type.delete()

    def test_remove_metadata_view(self):
        document_metadata = self.document.metadata.create(
            metadata_type=self.metadata_type, value=''
        )

        self.assertEqual(len(self.document.metadata.all()), 1)

        # Test display of metadata removal form
        response = self.client.get(
            reverse(
                'metadata:metadata_remove', args=(self.document.pk,),
            )
        )

        self.assertContains(response, 'emove', status_code=200)

        # Test post to metadata removal view
        response = self.client.post(
            reverse(
                'metadata:metadata_remove', args=(self.document.pk,),
            ), data={
                'form-0-id': document_metadata.metadata_type.pk,
                'form-0-update': True,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )

        self.assertContains(response, 'Success', status_code=200)

        self.assertEqual(len(self.document.metadata.all()), 0)

    def test_metadata_edit_after_document_type_change(self):
        # Gitlab issue #204
        # Problems to add required metadata after changin the document type

        document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2
        )

        metadata_type_2 = MetadataType.objects.create(
            name=TEST_METADATA_TYPE_NAME_2, label=TEST_METADATA_TYPE_LABEL_2
        )

        document_metadata_2 = document_type_2.metadata.create(
            metadata_type=metadata_type_2, required=True
        )

        self.document.set_document_type(document_type=document_type_2)

        response = self.client.get(
            reverse(
                'metadata:metadata_edit', args=(self.document.pk,),
            ), follow=True
        )

        self.assertContains(response, 'Edit', status_code=200)

        response = self.client.post(
            reverse(
                'metadata:metadata_edit', args=(self.document.pk,),
            ), data={
                'form-0-id': document_metadata_2.pk,
                'form-0-update': True,
                'form-0-value': TEST_DOCUMENT_METADATA_VALUE_2,
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }, follow=True
        )

        self.assertContains(response, 'Metadata for document', status_code=200)

        self.assertEqual(
            self.document.metadata.get(metadata_type=metadata_type_2
        ).value, TEST_DOCUMENT_METADATA_VALUE_2)
