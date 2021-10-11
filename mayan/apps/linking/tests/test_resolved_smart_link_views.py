from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_resolved_smart_link_view

from .mixins import (
    ResolvedSmartLinkDocumentViewTestMixin, SmartLinkTestMixin
)


class ResolvedSmartLinkDocumentViewTestCase(
    SmartLinkTestMixin, ResolvedSmartLinkDocumentViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        self._create_test_document_stub()
        self._create_test_document_stub(label='linked')
        self._create_test_smart_link(add_test_document_type=True)
        self._create_test_smart_link_condition()

    def test_document_resolved_smart_link_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_resolved_smart_link_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_documents[0].uuid
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_link_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].uuid
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_link_list_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_documents[0].uuid
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_link_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].uuid
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_resolved_smart_link_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )

        self.test_documents[0].delete()

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_list_view()
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=404,
            text=self.test_documents[0].uuid
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_document_list_with_no_permission(self):
        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_document_list_with_main_document_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_document_list_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_document_list_with_main_document_and_smart_link_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, text=self.test_documents[1].label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_main_document_resolved_smart_document_list_with_main_document_and_smart_link_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self.test_documents[0].delete()

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_resolved_smart_document_list_with_full_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response=response, text=self.test_documents[1].label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_linked_document_resolved_smart_document_list_with_full_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self.test_documents[1].delete()

        self._clear_events()

        response = self._request_test_document_resolved_smart_link_document_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, text=self.test_documents[1].label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
