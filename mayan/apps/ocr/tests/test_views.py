from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_ocr_document_version_content_deleted,
    event_ocr_document_version_submitted, event_ocr_document_version_finished
)
from ..models import DocumentVersionPageOCRContent
from ..permissions import (
    permission_document_version_ocr_content_view,
    permission_document_version_ocr, permission_document_type_ocr_setup
)
from ..utils import get_instance_ocr_content

from .literals import TEST_DOCUMENT_VERSION_OCR_CONTENT
from .mixins import (
    DocumentVersionOCRTestMixin, DocumentVersionOCRViewTestMixin,
    DocumentVersionPageOCRViewTestMixin, DocumentTypeOCRViewTestMixin
)


class DocumentTypeOCRViewsTestCase(
    DocumentTypeOCRViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_ocr_settings_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_ocr_settings_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_ocr_setup
        )

        self._clear_events()

        response = self._request_test_document_type_ocr_settings_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_submit_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_document_type_ocr_submit_view()
        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_submit_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_document_type_ocr_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
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

    def test_trashed_document_type_ocr_submit_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_type_ocr_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionOCRViewsTestCase(
    DocumentVersionOCRTestMixin, DocumentVersionOCRViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_content_delete_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self.test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_content_delete_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_content_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self.test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].target, self.test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_content_deleted.id
        )

    def test_trashed_document_content_delete_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self.test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_content_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_content_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_content_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_VERSION_OCR_CONTENT,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_content_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_submit_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ''.join(self.test_document_version.ocr_content()), ''
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_submit_view_with_access(self):
        self.grant_access(
            permission=permission_document_version_ocr, obj=self.test_document
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
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

    def test_trashed_document_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_multiple_document_submit_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_multiple_ocr_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ''.join(self.test_document_version.ocr_content()), ''
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_multiple_document_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_multiple_ocr_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
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

    def test_trashed_document_multiple_document_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_multiple_ocr_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self.test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_ocr_download_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_ocr_download_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.expected_content_types = ('text/html; charset=utf-8',)

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=(
                ''.join(get_instance_ocr_content(instance=self.test_document))
            ),
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_ocr_download_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_ocr_error_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_ocr_error_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_ocr_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_error_list_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_ocr_error_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_version_ocr
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_error_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageOCRViewsTestCase(
    DocumentVersionOCRTestMixin, DocumentVersionPageOCRViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_page_content_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_page_content_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_VERSION_OCR_CONTENT,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_page_content_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_ocr_content_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
