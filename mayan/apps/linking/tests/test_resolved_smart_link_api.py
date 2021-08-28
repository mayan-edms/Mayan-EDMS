from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_resolved_smart_link_view

from .mixins import ResolvedSmartLinkAPIViewTestMixin, SmartLinkTestMixin


class ResolvedSmartLinkAPIViewTestCase(
    DocumentTestMixin, SmartLinkTestMixin,
    ResolvedSmartLinkAPIViewTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_smart_link(add_test_document_type=True)
        self._create_test_smart_link_condition()
        self._create_test_document_stub()
        self._create_test_document_stub(label='linked')

    def test_resolved_smart_link_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_detail_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_detail_api_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_detail_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'], str(self.test_documents[0].uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_resolved_smart_link_detail_api_view_with_full_access(self):
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

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_list_api_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_list_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['label'],
            str(self.test_documents[0].uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_resolved_smart_link_list_api_view_with_access(self):
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

        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_document_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_document_list_api_view_with_main_document_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_document_list_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_document_list_api_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_document_list_api_view_with_main_document_and_smart_link_access(self):
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_resolved_smart_link_view
        )
        self.grant_access(
            obj=self.test_smart_link,
            permission=permission_resolved_smart_link_view
        )

        self._clear_events()

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_resolved_smart_link_document_list_api_view_with_main_document_and_smart_link_access(self):
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

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_resolved_smart_link_document_list_api_view_with_full_access(self):
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

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_documents[1].label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_linked_document_resolved_smart_link_document_list_api_view_with_full_access(self):
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

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
