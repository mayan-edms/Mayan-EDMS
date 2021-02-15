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
    def test_document_version_page_create_api_view_no_permission(self):
        document_version_count_page = self.test_document.version_active.version_pages.count()

        self._clear_events()

        response = self._request_test_document_version_page_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.version_active.version_pages.count(),
            document_version_count_page
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version_page)
        self.assertEqual(events[0].verb, event_document_version_page_created.id)

    def test_document_version_page_delete_api_view_no_permission(self):
        document_version_count_page = self.test_document.version_active.version_pages.count()

        self._clear_events()

        response = self._request_test_document_version_page_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.version_active.version_pages.count(),
            document_version_count_page
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version)
        self.assertEqual(events[0].verb, event_document_version_page_deleted.id)

    def test_document_version_page_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_page_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_edit_via_patch_api_view_no_permission(self):
        document_version_page_number = self.test_document_version_page.page_number

        self._clear_events()

        response = self._request_test_document_version_page_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_version_page.refresh_from_db()
        self.assertEqual(
            self.test_document_version_page.page_number,
            document_version_page_number
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_edit_via_patch_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_page_number = self.test_document_version_page.page_number

        self._clear_events()

        response = self._request_test_document_version_page_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_version_page.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version_page.page_number,
            document_version_page_number
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version_page)
        self.assertEqual(events[0].verb, event_document_version_page_edited.id)

    def test_document_version_page_edit_via_put_api_view_no_permission(self):
        document_version_page_number = self.test_document_version_page.page_number

        self._clear_events()

        response = self._request_test_document_version_page_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_version_page.refresh_from_db()
        self.assertEqual(
            self.test_document_version_page.page_number,
            document_version_page_number
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_edit_via_put_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_page_number = self.test_document_version_page.page_number

        self._clear_events()

        response = self._request_test_document_version_page_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_version_page.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version_page.page_number,
            document_version_page_number
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_version_page)
        self.assertEqual(events[0].verb, event_document_version_page_edited.id)

    def test_document_version_page_image_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_image_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_image_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_page_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_version_page.id
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
