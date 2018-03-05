from __future__ import unicode_literals

from django.test import override_settings

from common.tests import BaseTestCase
from documents.models import DocumentType
from documents.permissions import permission_document_view
from documents.search import document_search, document_page_search
from documents.tests import TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_PATH


@override_settings(OCR_AUTO_OCR=False)
class DocumentSearchTestCase(BaseTestCase):
    def setUp(self):
        super(DocumentSearchTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object, label='mayan_11_1.pdf'
            )

    def tearDown(self):
        self.document_type.delete()
        super(DocumentSearchTestCase, self).tearDown()

    def _perform_document_page_search(self):
        return document_page_search.search(
            {'q': self.document.label}, user=self.user
        )

    def _perform_document_search(self):
        return document_search.search(
            {'q': self.document.label}, user=self.user
        )

    def test_document_page_search_no_access(self):
        queryset, elapsed_time = self._perform_document_page_search()
        self.assertFalse(self.document.pages.first() in queryset)

    def test_document_page_search_with_access(self):
        self.grant_access(permission=permission_document_view, obj=self.document)
        queryset, elapsed_time = self._perform_document_page_search()
        self.assertTrue(self.document.pages.first() in queryset)

    def test_document_search_no_access(self):
        queryset, elapsed_time = self._perform_document_search()
        self.assertFalse(self.document in queryset)

    def test_document_search_with_access(self):
        self.grant_access(permission=permission_document_view, obj=self.document)
        queryset, elapsed_time = self._perform_document_search()
        self.assertTrue(self.document in queryset)
