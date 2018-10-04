from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase
from documents.search import document_search
from documents.tests import (
    DocumentTestMixin, TEST_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_FILENAME
)


@override_settings(OCR_AUTO_OCR=False)
class DocumentSearchTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False
    test_document_filename = TEST_DOCUMENT_FILENAME

    def test_simple_search_after_related_name_change(self):
        """
        Test that simple search works after related_name changes to
        document versions and document version pages
        """
        self.document = self.upload_document()
        queryset, elapsed_time = document_search.search(
            {'q': 'Mayan'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.document in queryset)

    def test_advanced_search_after_related_name_change(self):
        # Test versions__filename
        self.document = self.upload_document()
        queryset, elapsed_time = document_search.search(
            {'label': self.document.label}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.document in queryset)

        # Test versions__mimetype
        queryset, elapsed_time = document_search.search(
            {'versions__mimetype': self.document.file_mimetype},
            user=self.admin_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.document in queryset)

    def test_simple_or_search(self):
        self.document = self.upload_document()
        self.test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
        self.document_2 = self.upload_document()
        self.document_2.label = 'second_doc.pdf'
        self.document_2.save()

        queryset, elapsed_time = document_search.search(
            {'q': 'Mayan OR second'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.document in queryset)
        self.assertTrue(self.document_2 in queryset)

    def test_simple_and_search(self):
        self.test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
        self.document_2 = self.upload_document()
        self.document_2.label = 'second_doc.pdf'
        self.document_2.save()

        queryset, elapsed_time = document_search.search(
            {'q': 'non_valid second'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset, elapsed_time = document_search.search(
            {'q': 'second non_valid'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_simple_negated_search(self):
        self.test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
        self.document_2 = self.upload_document()
        self.document_2.label = 'second_doc.pdf'
        self.document_2.save()

        queryset, elapsed_time = document_search.search(
            {'q': '-non_valid second'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset, elapsed_time = document_search.search(
            {'label': '-second'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset, elapsed_time = document_search.search(
            {'label': '-second -Mayan'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset, elapsed_time = document_search.search(
            {'label': '-second OR -Mayan'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset, elapsed_time = document_search.search(
            {'label': '-non_valid -second'}, user=self.admin_user
        )
        self.assertEqual(queryset.count(), 0)
