from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_ocr_document_version_finished,
    event_ocr_document_version_submitted
)
from ..permissions import permission_document_version_ocr

from .mixins import DocumentOCRAPIViewTestMixin


class DocumentOCRAPIViewTestCase(
    DocumentTestMixin, DocumentOCRAPIViewTestMixin, BaseAPITestCase
):
    def test_document_ocr_submit_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_ocr_submit_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(
            hasattr(self.test_document.pages.first(), 'ocr_content')
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_ocr_submit_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_ocr_submit_api_view()
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

    def test_trashed_document_ocr_submit_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_ocr_submit_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
