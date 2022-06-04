from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.search import search_model_document
from mayan.apps.dynamic_search.tests.mixins import SearchTestMixin

from .mixins import TagTestMixin


class DocumentTagSearchTestCase(
    TagTestMixin, SearchTestMixin, GenericDocumentViewTestCase
):
    _test_tag_add_test_document = True
    auto_create_test_tag = True

    def _do_test_search(self):
        return self.search_backend.search(
            search_model=search_model_document, query={
                'tags__label': self._test_tag.label
            }, user=self._test_case_user
        )

    def test_search_model_document_no_permission(self):
        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_search_model_document_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_document in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_search_model_document_with_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        queryset = self._do_test_search()
        self.assertTrue(self._test_document not in queryset)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
