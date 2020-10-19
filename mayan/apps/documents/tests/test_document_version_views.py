from django.contrib.contenttypes.models import ContentType

from mayan.apps.storage.models import DownloadFile

from ..literals import DOCUMENT_FILE_ACTION_PAGES_KEEP
from ..permissions import (
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_print, permission_document_version_view
)

from .base import GenericDocumentViewTestCase
from .mixins.document_version_mixins import (
    DocumentVersionPageRemapViewTestMixin,
    DocumentVersionPageResetViewTestMixin, DocumentVersionViewTestMixin
)


class DocumentVersionViewTestCase(
    DocumentVersionViewTestMixin, GenericDocumentViewTestCase
):
    def test_document_version_edit_view_no_permission(self):
        document_version_comment = self.test_document_version.comment

        response = self._request_test_document_version_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_version.refresh_from_db()
        self.assertEqual(
            self.test_document_version.comment,
            document_version_comment
        )

    def test_document_version_edit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        document_version_comment = self.test_document_version.comment

        response = self._request_test_document_version_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_version.refresh_from_db()
        self.assertNotEqual(
            self.test_document_version.comment,
            document_version_comment
        )

    def test_document_version_export_view_no_permission(self):
        download_file_count = DownloadFile.objects.count()

        response = self._request_test_document_version_export_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count
        )

    def test_document_version_export_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_export
        )

        download_file_count = DownloadFile.objects.count()

        response = self._request_test_document_version_export_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count + 1
        )

    def test_document_version_list_view_no_permission(self):
        response = self._request_test_document_version_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_version)
        )

    def test_document_version_preview_view_no_permission(self):
        response = self._request_test_document_version_preview_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_preview_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_view
        )

        response = self._request_test_document_version_preview_view()
        self.assertContains(
            response=response, status_code=200,
            text=str(self.test_document_version)
        )

    def test_document_version_print_form_view_no_permission(self):
        response = self._request_test_document_version_print_form_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_print_form_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_print
        )

        response = self._request_test_document_version_print_form_view()
        self.assertEqual(response.status_code, 200)

    def test_document_version_print_view_no_permission(self):
        response = self._request_test_document_version_print_view()
        self.assertEqual(response.status_code, 404)

    def test_document_version_print_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_print
        )

        response = self._request_test_document_version_print_view()
        self.assertEqual(response.status_code, 200)


class DocumentVersionPageRemapViewTestCase(
    DocumentVersionPageRemapViewTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._upload_test_document_file()
        self.test_document_file_pages = []
        self.source_content_types = []
        self.source_object_ids = []

        for test_document_file in self.test_document.files.all():
            for test_document_file_page in test_document_file.pages.all():
                self.test_document_file_pages.append(test_document_file_page)
                self.source_content_types.append(
                    ContentType.objects.get_for_model(
                        model=test_document_file_page
                    )
                )
                self.source_object_ids.append(test_document_file_page.pk)

        self.single_page_remap_data = {
            'form-0-source_content_type': self.source_content_types[0].pk,
            'form-0-source_object_id': self.source_object_ids[0],
            'form-0-source_page_number': '1',
            'form-0-target_page_number': '1',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        self.repeated_page_number_remap_data = {
            'form-0-source_content_type': self.source_content_types[0].pk,
            'form-0-source_object_id': self.source_object_ids[0],
            'form-0-source_page_number': '1',
            'form-0-target_page_number': '1',
            'form-1-source_content_type': self.source_content_types[1].pk,
            'form-1-source_object_id': self.source_object_ids[1],
            'form-1-source_page_number': '1',
            'form-1-target_page_number': '1',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }

    def test_document_version_remap_view_no_permission(self):
        response = self._request_test_document_version_page_list_remap_view(
            data=self.single_page_remap_data
        )
        self.assertEqual(response.status_code, 404)

        self.test_document_version.refresh_from_db()

        self.assertNotEqual(
            self.test_document_version.pages.first().content_object,
            self.test_document_file_pages[0]
        )
        self.assertEqual(
            self.test_document_version.pages.first().content_object,
            self.test_document_file_pages[1]
        )

    def test_document_version_remap_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        response = self._request_test_document_version_page_list_remap_view(
            data=self.single_page_remap_data
        )
        self.assertEqual(response.status_code, 302)

        self.test_document_version.refresh_from_db()

        self.assertEqual(
            self.test_document_version.pages.first().content_object,
            self.test_document_file_pages[0]
        )
        self.assertNotEqual(
            self.test_document_version.pages.first().content_object,
            self.test_document_file_pages[1]
        )

    def test_document_version_remap_repeated_target_page_number_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        response = self._request_test_document_version_page_list_remap_view(
            data=self.repeated_page_number_remap_data
        )
        self.assertEqual(response.status_code, 200)

        self.test_document_version.refresh_from_db()

        self.assertNotEqual(
            self.test_document_version.pages.first().content_object,
            self.test_document_file_pages[0]
        )
        self.assertEqual(
            self.test_document_version.pages.first().content_object,
            self.test_document_file_pages[1]
        )


class DocumentVersionPageResetViewTestCase(
    DocumentVersionPageResetViewTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._upload_test_document_file(
            action=DOCUMENT_FILE_ACTION_PAGES_KEEP
        )
        self.test_document_file_pages = []
        self.source_content_types = []
        self.source_object_ids = []

        for test_document_file in self.test_document.files.all():
            for test_document_file_page in test_document_file.pages.all():
                self.test_document_file_pages.append(test_document_file_page)
                self.source_content_types.append(
                    ContentType.objects.get_for_model(
                        model=test_document_file_page
                    )
                )
                self.source_object_ids.append(test_document_file_page.pk)

    def test_document_version_reset_view_no_permission(self):
        response = self._request_test_document_version_page_list_reset_view()
        self.assertEqual(response.status_code, 404)

        self.test_document_version.refresh_from_db()

        self.assertEqual(
            self.test_document_version.pages.all()[0].content_object,
            self.test_document_file_pages[0]
        )

    def test_document_version_reset_view_with_access(self):
        self.grant_access(
            obj=self.test_document_version,
            permission=permission_document_version_edit
        )

        response = self._request_test_document_version_page_list_reset_view()
        self.assertEqual(response.status_code, 302)

        self.test_document_version.refresh_from_db()

        self.assertEqual(
            self.test_document_version.pages.all()[0].content_object,
            self.test_document_file_pages[1]
        )
