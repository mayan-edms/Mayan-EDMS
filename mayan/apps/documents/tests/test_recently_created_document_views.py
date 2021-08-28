from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase
from .mixins.recently_created_document_mixins import RecentlyCreatedDocumentViewTestMixin


class RecentlyCreatedDocumentViewTestCase(
    RecentlyCreatedDocumentViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()

    def test_recently_created_document_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_recently_created_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_recently_created_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_recently_created_document_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_recently_created_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.test_document.delete()

        self._clear_events()

        response = self._request_test_recently_created_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
