from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import document_search
from mayan.apps.documents.tests import DocumentTestMixin


class Issue46TestCase(DocumentTestMixin, GenericViewTestCase):
    """
    Functional tests to make sure issue 46 is fixed
    """
    auto_upload_document = False

    def setUp(self):
        super(Issue46TestCase, self).setUp()
        self.test_document_count = 4

        # Upload many instances of the same test document
        for i in range(self.test_document_count):
            self.upload_document()

    def test_advanced_search_past_first_page(self):
        test_document_label = self.test_documents[0].label

        for document in self.test_documents:
            self.grant_access(
                obj=document, permission=permission_document_view
            )

        # Make sure all documents are returned by the search
        queryset = document_search.search(
            {'label': test_document_label}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), self.test_document_count)

        with self.settings(COMMON_PAGINATE_BY=2):
            # Functional test for the first page of advanced results
            response = self.get(
                viewname='search:results',
                kwargs={'search_model': document_search.get_full_name()},
                data={'label': test_document_label}
            )

            # Total (1 - 2 out of 4) (Page 1 of 2)
            # 4 results total, 2 pages, current page is 1,
            # object in this page: 2
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['paginator'].object_list.count(), 4
            )
            self.assertEqual(response.context['paginator'].num_pages, 2)
            self.assertEqual(response.context['page_obj'].number, 1)
            self.assertEqual(
                response.context['page_obj'].object_list.count(), 2
            )

            # Functional test for the second page of advanced results
            response = self.get(
                viewname='search:results',
                kwargs={'search_model': document_search.get_full_name()},
                data={'label': test_document_label, 'page': 2}
            )

            # Total (3 - 4 out of 4) (Page 2 of 2)
            # 4 results total, 2 pages, current page is 1,
            # object in this page: 2
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['paginator'].object_list.count(), 4
            )
            self.assertEqual(response.context['paginator'].num_pages, 2)
            self.assertEqual(response.context['page_obj'].number, 2)
            self.assertEqual(
                response.context['page_obj'].object_list.count(), 2
            )
