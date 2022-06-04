from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import (
    TEST_FILE_HYBRID_PDF_CONTENT, TEST_FILE_HYBRID_PDF_FILENAME
)

from ..events import (
    event_parsing_document_file_content_deleted,
    event_parsing_document_file_finished,
    event_parsing_document_file_submitted
)
from ..models import DocumentFilePageContent
from ..permissions import (
    permission_document_file_content_view, permission_document_file_parse,
    permission_document_type_parsing_setup
)

from .mixins import (
    DocumentFileContentTestMixin, DocumentFileContentToolsViewTestMixin,
    DocumentFileContentViewTestMixin, DocumentTypeContentViewTestMixin
)


class DocumentFileContentViewTestCase(
    DocumentFileContentViewTestMixin, DocumentFileContentTestMixin,
    GenericDocumentViewTestCase
):
    auto_create_test_document_file_parsed_content = True

    def test_document_file_content_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_content_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_content_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_content_view
        )

        self._clear_events()

        response = self._request_test_document_file_content_view()
        self.assertContains(
            response=response, text=TEST_FILE_HYBRID_PDF_CONTENT,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_content_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_content_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_content_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_content_single_delete_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_content_single_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentFilePageContent.objects.filter(
                document_file_page=self._test_document_file.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_content_single_delete_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._clear_events()

        response = self._request_test_document_file_content_single_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentFilePageContent.objects.filter(
                document_file_page=self._test_document_file.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_file)
        self.assertEqual(
            events[0].verb, event_parsing_document_file_content_deleted.id
        )

    def test_trashed_document_file_content_single_delete_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_content_single_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentFilePageContent.objects.filter(
                document_file_page=self._test_document_file.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_content_multiple_delete_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_content_multiple_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentFilePageContent.objects.filter(
                document_file_page=self._test_document_file.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_content_multiple_delete_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._clear_events()

        response = self._request_test_document_file_content_multiple_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            DocumentFilePageContent.objects.filter(
                document_file_page=self._test_document_file.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_file)
        self.assertEqual(
            events[0].verb, event_parsing_document_file_content_deleted.id
        )

    def test_trashed_document_file_content_multiple_delete_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_content_multiple_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            DocumentFilePageContent.objects.filter(
                document_file_page=self._test_document_file.pages.first()
            ).exists()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentFilePageContentViewTestCase(
    DocumentFileContentViewTestMixin, DocumentFileContentTestMixin,
    GenericDocumentViewTestCase
):
    auto_create_test_document_file_parsed_content = True

    def test_document_file_page_content_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_page_content_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_page_content_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_content_view
        )

        self._clear_events()

        response = self._request_test_document_file_page_content_view()
        self.assertContains(
            response=response, text=TEST_FILE_HYBRID_PDF_CONTENT,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_page_content_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_content_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_page_content_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentFileContentParsingViewTestCase(
    DocumentFileContentViewTestMixin, GenericDocumentViewTestCase
):
    _skip_file_descriptor_test = True

    def test_document_file_parsing_download_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_content_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_parsing_download_view_with_access(self):
        self.expected_content_types = ('application/octet-stream',)

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_content_view
        )

        self._clear_events()

        response = self._request_test_document_file_content_download_view()
        self.assertEqual(response.status_code, 200)

        self.assert_download_response(
            response=response, content=''.join(
                self._test_document_file.content()
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_parsing_download_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_content_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_content_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_parsing_submit_single_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_parsing_submit_single_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._clear_events()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_file)
        self.assertEqual(
            events[0].verb, event_parsing_document_file_submitted.id
        )

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_file)
        self.assertEqual(
            events[1].verb, event_parsing_document_file_finished.id
        )

    def test_trashed_document_file_parsing_single_submit_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_parsing_submit_multiple_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_parsing_submit_multiple_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._clear_events()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_file)
        self.assertEqual(
            events[0].verb, event_parsing_document_file_submitted.id
        )

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_file)
        self.assertEqual(
            events[1].verb, event_parsing_document_file_finished.id
        )

    def test_trashed_document_file_parsing_multiple_submit_view_with_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_parse
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_parsing_submit_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class DocumentTypeParsingViewTestCase(
    DocumentFileContentToolsViewTestMixin, GenericDocumentViewTestCase
):
    _skip_file_descriptor_test = True
    _test_document_filename = TEST_FILE_HYBRID_PDF_FILENAME
    auto_upload_test_document = False

    def _get_document_file_content(self):
        return ''.join(
            self._test_document_file.content()
        )

    def test_document_type_parsing_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_document_type_parsing_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, status_code=200,
            text=self._test_document_type.label
        )

        self.assertNotEqual(
            self._get_document_file_content(), TEST_FILE_HYBRID_PDF_CONTENT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_view_with_permission(self):
        self.grant_permission(permission=permission_document_file_parse)

        self._upload_test_document()

        self._clear_events()

        response = self._request_document_type_parsing_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._get_document_file_content(), TEST_FILE_HYBRID_PDF_CONTENT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, self._test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document_file)
        self.assertEqual(
            events[0].verb, event_parsing_document_file_submitted.id
        )

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_file)
        self.assertEqual(
            events[1].verb, event_parsing_document_file_finished.id
        )


class DocumentTypeContentViewTestCase(
    DocumentTypeContentViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_parsing_settings_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_parsing_settings_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_parsing_settings_view_with_access(self):
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_type_parsing_setup
        )

        self._clear_events()

        response = self._request_test_document_type_parsing_settings_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
