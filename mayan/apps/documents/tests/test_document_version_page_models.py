from ..literals import DOCUMENT_FILE_ACTION_PAGES_APPEND

from .base import GenericDocumentTestCase


class DocumentVersionPageTestCase(GenericDocumentTestCase):
    def test_version_pages_reset_no_file(self):
        self.test_document_file.delete()
        self.test_document_version.pages_reset()

    def test_version_pages_reset(self):
        self._upload_test_document_file(action=DOCUMENT_FILE_ACTION_PAGES_APPEND)

        test_document_version_page_content_objects = self.test_document.versions.last().page_content_objects

        self.test_document_version.pages_reset()

        self.assertNotEqual(
            self.test_document.versions.last().page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertEqual(
            self.test_document.versions.last().page_content_objects,
            list(self.test_document.file_latest.pages.all())
        )

    def test_method_get_absolute_url(self):
        self.assertTrue(
            self.test_document.version_active.pages.first().get_absolute_url()
        )
