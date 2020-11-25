from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_version_page_created, event_document_version_page_deleted,
    event_document_version_page_edited
)
from ..permissions import (
    permission_document_version_edit, permission_document_version_view
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_version_mixins import (
    DocumentVersionPageAPIViewTestMixin
)


class DocumentVersionPageAPIViewTestCase(
    DocumentVersionPageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    _test_event_object_name = 'test_document_version_page'

    def test_document_version_page_create_api_view_no_permission(self):
        document_version_count_page = self.test_document.version_active.version_pages.count()

        self._clear_events()

        response = self._request_test_document_version_page_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.version_active.version_pages.count(),
            document_version_count_page
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_page_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_count_page = self.test_document.version_active.version_pages.count()

        self._clear_events()

        response = self._request_test_document_version_page_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document.version_active.version_pages.count(),
            document_version_count_page + 1
        )

        event = self._get_test_object_event()
        self.assertEqual(event.action_object, self.test_document_version)
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_version_page)
        self.assertEqual(event.verb, event_document_version_page_created.id)

    def test_document_version_page_delete_api_view_no_permission(self):
        document_version_count_page = self.test_document.version_active.version_pages.count()

        self._clear_events()

        response = self._request_test_document_version_page_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.version_active.version_pages.count(),
            document_version_count_page
        )

        event = self._get_test_object_event(object_name='test_document_version')
        self.assertEqual(event, None)

    def test_document_version_page_delete_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_count_page = self.test_document.version_active.version_pages.count()

        self._clear_events()

        response = self._request_test_document_version_page_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.version_active.version_pages.count(),
            document_version_count_page - 1
        )

        event = self._get_test_object_event(object_name='test_document_version')
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_version)
        self.assertEqual(event.verb, event_document_version_page_deleted.id)

    def test_document_version_page_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_page_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_page_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_version_page_image_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)


    def test_document_version_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    #TODO:Edit views
    #TODO:List view
