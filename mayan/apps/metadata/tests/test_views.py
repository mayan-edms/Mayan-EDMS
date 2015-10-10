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

from .literals import TEST_METADATA_TYPE_NAME, TEST_METADATA_TYPE_LABEL


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
