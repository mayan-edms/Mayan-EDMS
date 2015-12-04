from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files.base import File
from django.test import TestCase

from documents.models import DocumentType
from documents.search import document_search
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from user_management.tests import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL
)


class DocumentSearchTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object), label='mayan_11_1.pdf'
            )

    def tearDown(self):
        self.document_type.delete()

    def test_simple_search_after_related_name_change(self):
        """
        Test that simple search works after related_name changes to
        document versions and document version pages
        """

        model_list, result_set, elapsed_time = document_search.search(
            {'q': 'Mayan'}, user=self.admin_user
        )
        self.assertEqual(len(result_set), 1)
        self.assertEqual(list(model_list), [self.document])

    def test_advanced_search_after_related_name_change(self):
        # Test versions__filename
        model_list, result_set, elapsed_time = document_search.search(
            {'label': self.document.label}, user=self.admin_user
        )
        self.assertEqual(len(result_set), 1)
        self.assertEqual(list(model_list), [self.document])

        # Test versions__mimetype
        model_list, result_set, elapsed_time = document_search.search(
            {'versions__mimetype': self.document.file_mimetype},
            user=self.admin_user
        )
        self.assertEqual(len(result_set), 1)
        self.assertEqual(list(model_list), [self.document])
