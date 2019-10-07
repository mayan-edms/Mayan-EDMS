from __future__ import unicode_literals

from django.utils.encoding import force_text

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests.mixins import DocumentTestMixin


class DocumentSearchTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_document = False

    def test_simple_search_after_related_name_change(self):
        """
        Test that simple search works after related_name changes to
        document versions and document version pages
        """
        self.upload_document(label='first_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = document_search.search(
            {'q': 'first'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_advanced_search_after_related_name_change(self):
        # Test versions__filename
        self.upload_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = document_search.search(
            {'label': self.test_document.label}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        # Test versions__mimetype
        queryset = document_search.search(
            {'versions__mimetype': self.test_document.file_mimetype},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_meta_only(self):
        self.upload_document(label='first_doc')
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        queryset = document_search.search(
            {'q': 'OR first'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

    def test_simple_or_search(self):
        self.upload_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self.upload_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        queryset = document_search.search(
            {'q': 'first OR second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_advanced_or_search(self):
        self.upload_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self.upload_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        queryset = document_search.search(
            {'label': 'first OR second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_simple_and_search(self):
        self.upload_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = document_search.search(
            {'q': 'non_valid second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = document_search.search(
            {'q': 'second non_valid'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_simple_negated_search(self):
        self.upload_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = document_search.search(
            {'q': '-non_valid second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = document_search.search(
            {'label': '-second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = document_search.search(
            {'label': '-second -Mayan'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = document_search.search(
            {'label': '-second OR -Mayan'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = document_search.search(
            {'label': '-non_valid -second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_with_dashed_content(self):
        self.upload_document(label='second-document')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = document_search.search(
            {'label': '-second-document'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = document_search.search(
            {'label': '-"second-document"'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_field_transformation_functions(self):
        self.upload_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = document_search.search(
            {'uuid': force_text(self.test_document.uuid)}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
