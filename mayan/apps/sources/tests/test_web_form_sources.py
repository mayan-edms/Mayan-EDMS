from django.core.files import File

from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_COMPRESSED_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_CHECKSUM,
    TEST_SMALL_DOCUMENT_PATH
)

from ..source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_ALWAYS

from .mixins.base_mixins import InteractiveSourceBackendTestMixin
from .mixins.web_form_source_mixins import WebFormSourceTestMixin


class WebFormSourceBackendTestCase(
    InteractiveSourceBackendTestMixin, WebFormSourceTestMixin,
    GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def _process_test_document(self, test_file_path=TEST_SMALL_DOCUMENT_PATH):
        source_backend_instance = self.test_source.get_backend_instance()

        with open(file=test_file_path, mode='rb') as file_object:
            self.test_forms = {
                'document_form': self.test_document_form,
                'source_form': InteractiveSourceBackendTestMixin.MockSourceForm(
                    file=File(file=file_object)
                ),
            }

            source_backend_instance.process_documents(
                document_type=self.test_document_type, forms=self.test_forms,
                request=self.get_test_request()
            )

    def test_upload_simple_file(self):
        self._create_test_web_form_source()

        document_count = Document.objects.count()

        self._process_test_document()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_SMALL_DOCUMENT_CHECKSUM
        )

    def test_upload_compressed_file(self):
        self._create_test_web_form_source(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_ALWAYS}
        )

        document_count = Document.objects.count()

        self._process_test_document(
            test_file_path=TEST_COMPRESSED_DOCUMENT_PATH
        )

        self.assertEqual(Document.objects.count(), document_count + 2)

        self.assertTrue(
            'first document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )
        self.assertTrue(
            'second document.pdf' in Document.objects.values_list(
                'label', flat=True
            )
        )
