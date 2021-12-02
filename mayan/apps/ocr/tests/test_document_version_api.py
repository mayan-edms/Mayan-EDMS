from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_ocr_document_version_page_content_edited,
    event_ocr_document_version_finished,
    event_ocr_document_version_submitted
)
from ..permissions import (
    permission_document_version_ocr,
    permission_document_version_ocr_content_edit,
    permission_document_version_ocr_content_view
)

from .literals import TEST_DOCUMENT_VERSION_OCR_CONTENT
from .mixins import (
    DocumentVersionOCRAPIViewTestMixin, DocumentVersionOCRTestMixin,
    DocumentVersionPageOCRAPIViewTestMixin
)


class DocumentVersionOCRAPIViewTestCase(
    DocumentTestMixin, DocumentVersionOCRAPIViewTestMixin, BaseAPITestCase
):
    def test_document_version_ocr_submit_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_ocr_submit_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_submit_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_submit_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertTrue(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].target, self.test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_submitted.id
        )

        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].target, self.test_document_version)
        self.assertEqual(
            events[1].verb, event_ocr_document_version_finished.id
        )

    def test_trashed_document_version_ocr_submit_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_submit_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageOCRAPIViewTestCase(
    DocumentTestMixin, DocumentVersionOCRTestMixin,
    DocumentVersionPageOCRAPIViewTestMixin, BaseAPITestCase
):
    def test_document_version_page_content_detail_api_view_via_get_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_api_view_via_get()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_content_detail_api_view_via_get_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_api_view_via_get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in response.data['content']
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_page_content_detail_api_view_via_get_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self.test_document.delete()
        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_api_view_via_get()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_content_edit_api_view_via_patch_no_permission(self):
        self._create_test_document_version_ocr_content()

        test_document_version_page_ocr_content = self.test_document_version_page.ocr_content.content

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_version_page.ocr_content.refresh_from_db()
        self.assertEqual(
            self.test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_content_edit_api_view_via_patch_with_access(self):
        self._create_test_document_version_ocr_content()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_edit
        )
        test_document_version_page_ocr_content = self.test_document_version_page.ocr_content.content

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_version_page.ocr_content.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].target, self.test_document_version_page)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_page_content_edited.id
        )

    def test_trashed_document_version_page_content_edit_api_view_via_patch_with_access(self):
        self._create_test_document_version_ocr_content()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_edit
        )
        test_document_version_page_ocr_content = self.test_document_version_page.ocr_content.content

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_api_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_version_page.ocr_content.refresh_from_db()
        self.assertEqual(
            self.test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_content_edit_api_view_via_put_no_permission(self):
        self._create_test_document_version_ocr_content()

        test_document_version_page_ocr_content = self.test_document_version_page.ocr_content.content

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_version_page.ocr_content.refresh_from_db()
        self.assertEqual(
            self.test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_content_edit_api_view_via_put_with_access(self):
        self._create_test_document_version_ocr_content()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_edit
        )
        test_document_version_page_ocr_content = self.test_document_version_page.ocr_content.content

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_version_page.ocr_content.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].target, self.test_document_version_page)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_page_content_edited.id
        )

    def test_trashed_document_version_page_content_edit_api_view_via_put_with_access(self):
        self._create_test_document_version_ocr_content()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_edit
        )
        test_document_version_page_ocr_content = self.test_document_version_page.ocr_content.content

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_api_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_version_page.ocr_content.refresh_from_db()
        self.assertEqual(
            self.test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
