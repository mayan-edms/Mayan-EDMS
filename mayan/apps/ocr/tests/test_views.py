from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_ocr_document_version_content_deleted,
    event_ocr_document_version_page_content_edited,
    event_ocr_document_version_submitted, event_ocr_document_version_finished
)
from ..models import DocumentVersionPageOCRContent
from ..permissions import (
    permission_document_version_ocr_content_edit,
    permission_document_version_ocr_content_view,
    permission_document_version_ocr, permission_document_type_ocr_setup
)

from .literals import TEST_DOCUMENT_VERSION_OCR_CONTENT
from .mixins import (
    DocumentVersionOCRTestMixin, DocumentVersionOCRViewTestMixin,
    DocumentVersionPageOCRViewTestMixin, DocumentTypeOCRViewTestMixin
)


class DocumentTypeOCRViewTestCase(
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
            obj=self._test_document_type,
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
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_ocr_submit_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_document_type_ocr_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_submitted.id
        )

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_version)
        self.assertEqual(
            events[1].verb, event_ocr_document_version_finished.id
        )

    def test_trashed_document_type_ocr_submit_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_version_ocr
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_document_type_ocr_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionOCRViewTestCase(
    DocumentVersionOCRTestMixin, DocumentVersionOCRViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_verions_ocr_content_single_delete_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_single_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self._test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_content_single_delete_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_content_single_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self._test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_content_deleted.id
        )

    def test_trashed_document_version_ocr_content_single_delete_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_single_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self._test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_content_multiple_delete_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_multiple_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self._test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_content_multiple_delete_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_content_multiple_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self._test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_content_deleted.id
        )

    def test_trashed_document_version_ocr_content_multiple_delete_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document, permission=permission_document_version_ocr
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_multiple_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentVersionPageOCRContent.objects.filter(
                document_version_page=self._test_document_version.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_content_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_content_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_content_detail_view()
        self.assertContains(
            response=response, text=TEST_DOCUMENT_VERSION_OCR_CONTENT,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_ocr_content_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_submit_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_ocr_single_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ''.join(self._test_document_version.ocr_content()), ''
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_submit_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_single_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_submitted.id
        )

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_version)
        self.assertEqual(
            events[1].verb, event_ocr_document_version_finished.id
        )

    def test_trashed_document_version_ocr_submit_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_single_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_multiple_submit_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_version_ocr_multiple_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            ''.join(self._test_document_version.ocr_content()), ''
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_multiple_submit_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_multiple_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_version)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_submitted.id
        )

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_version)
        self.assertEqual(
            events[1].verb, event_ocr_document_version_finished.id
        )

    def test_trashed_document_version_ocr_multiple_submit_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_multiple_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            TEST_DOCUMENT_VERSION_OCR_CONTENT in ''.join(
                self._test_document_version.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_download_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_ocr_download_view_with_access(self):
        self.expected_content_types = ('application/octet-stream',)

        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._clear_events()

        response = self._request_test_document_version_ocr_content_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=''.join(
                self._test_document.ocr_content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_ocr_download_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_ocr_content_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentVersionPageOCRViewTestCase(
    DocumentVersionOCRTestMixin, DocumentVersionPageOCRViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_document_version_page_ocr_content_detail_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_ocr_content_detail_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
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

    def test_trashed_document_version_page_ocr_content_detail_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_ocr_content_edit_view_no_permission(self):
        self._create_test_document_version_ocr_content()

        test_document_version_page_ocr_content = self._test_document_version_page.ocr_content.content
        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_document_version_page.ocr_content.refresh_from_db()
        self.assertEqual(
            self._test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_version_page_ocr_content_edit_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_edit
        )

        test_document_version_page_ocr_content = self._test_document_version_page.ocr_content.content
        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_document_version_page.ocr_content.refresh_from_db()
        self.assertNotEqual(
            self._test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_version_page)
        self.assertEqual(
            events[0].verb, event_ocr_document_version_page_content_edited.id
        )

    def test_trashed_document_version_page_ocr_content_edit_view_with_access(self):
        self._create_test_document_version_ocr_content()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_version_ocr_content_edit
        )

        test_document_version_page_ocr_content = self._test_document_version_page.ocr_content.content
        self._test_document.delete()
        self._clear_events()

        response = self._request_test_document_version_page_ocr_content_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_document_version_page.ocr_content.refresh_from_db()
        self.assertEqual(
            self._test_document_version_page.ocr_content.content,
            test_document_version_page_ocr_content
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
