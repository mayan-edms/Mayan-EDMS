from ..literals import (
    DOCUMENT_FILE_ACTION_PAGES_NEW, DOCUMENT_FILE_ACTION_PAGES_APPEND,
    DOCUMENT_FILE_ACTION_PAGES_KEEP
)

from .base import GenericDocumentTestCase


class DocumentVersionTestCase(GenericDocumentTestCase):
    def test_version_new_file_new_pages(self):
        test_document_version_page_content_objects = self.test_document_version.page_content_objects

        self.assertEqual(self.test_document.versions.count(), 1)

        self._upload_test_document_file(action=DOCUMENT_FILE_ACTION_PAGES_NEW)

        self.assertEqual(self.test_document.versions.count(), 2)

        self.assertNotEqual(
            self.test_document_version.page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertEqual(
            self.test_document_version.page_content_objects,
            list(self.test_document.file_latest.pages.all())
        )

    def test_version_new_version_keep_pages(self):
        test_document_version_page_content_objects = self.test_document_version.page_content_objects

        self.assertEqual(self.test_document.versions.count(), 1)

        self._upload_test_document_file(action=DOCUMENT_FILE_ACTION_PAGES_KEEP)

        self.assertEqual(self.test_document.versions.count(), 1)

        self.assertEqual(
            self.test_document_version.page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertNotEqual(
            self.test_document_version.page_content_objects,
            list(self.test_document.file_latest.pages.all())
        )

    def test_version_new_file_append_pages(self):
        test_document_version_page_content_objects = self.test_document_version.page_content_objects

        self.assertEqual(self.test_document.versions.count(), 1)
        self.assertEqual(self.test_document.files.count(), 1)

        self._upload_test_document_file(action=DOCUMENT_FILE_ACTION_PAGES_APPEND)

        self.assertEqual(self.test_document.files.count(), 2)
        self.assertEqual(self.test_document.versions.count(), 2)

        test_document_version_expected_page_content_objects = list(
            self.test_document.files.first().pages.all()
        )
        test_document_version_expected_page_content_objects.extend(
            list(
                self.test_document.files.last().pages.all()
            )
        )

        self.assertNotEqual(
            self.test_document_version.page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertEqual(
            self.test_document_version.page_content_objects,
            test_document_version_expected_page_content_objects
        )

    def test_method_get_absolute_url(self):
        self.assertTrue(self.test_document.version_active.get_absolute_url())
