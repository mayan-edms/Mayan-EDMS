from pathlib import Path

from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_SMALL_DOCUMENT_CHECKSUM, TEST_SMALL_DOCUMENT_PATH
)

from .mixins.base_mixins import InteractiveSourceBackendTestMixin
from .mixins.staging_folder_source_mixins import StagingFolderTestMixin


class StagingFolderSourceBackendTestCase(
    StagingFolderTestMixin, InteractiveSourceBackendTestMixin,
    GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def _process_test_document(self, test_file_path=TEST_SMALL_DOCUMENT_PATH):
        source_backend_instance = self.test_source.get_backend_instance()

        self.test_forms = {
            'document_form': self.test_document_form,
            'source_form': InteractiveSourceBackendTestMixin.MockSourceForm(
                staging_folder_file_id=self.test_staging_folder_file.encoded_filename
            ),
        }

        source_backend_instance.process_documents(
            document_type=self.test_document_type, forms=self.test_forms,
            request=self.get_test_request()
        )

    def test_upload_simple_file(self):
        self._create_test_staging_folder()

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._process_test_document()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_delete_after_upload(self):
        self._create_test_staging_folder(
            extra_data={'delete_after_upload': True}
        )

        self._copy_test_staging_folder_document()

        document_count = Document.objects.count()

        self._process_test_document()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

        path = Path(self.test_source.get_backend_data()['folder_path'])

        self.assertEqual(sum(1 for x in path.glob('*') if x.is_file()), 0)
