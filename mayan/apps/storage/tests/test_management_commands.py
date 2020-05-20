from django.core import management
from django.utils.encoding import force_text

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.mimetype.api import get_mimetype

from .mixins import StorageProcessorTestMixin


class StorageProcessManagementCommandTestCase(
    StorageProcessorTestMixin, GenericDocumentTestCase
):
    def _call_command(self, reverse=None):
        options = {
            'app_label': 'documents',
            'defined_storage_name': 'documents__documentversion',
            'log_file': force_text(self.path_test_file),
            'model_name': 'DocumentVersion',
            'reverse': reverse
        }
        management.call_command(command_name='storage_process', **options)

    def _upload_and_call(self):
        self.defined_storage.dotted_path = 'django.core.files.storage.FileSystemStorage'
        self.defined_storage.kwargs = {
            'location': self.document_storage_kwargs['location']
        }

        self._upload_test_document()

        self.defined_storage.dotted_path = 'mayan.apps.storage.backends.compressedstorage.ZipCompressedPassthroughStorage'
        self.defined_storage.kwargs = {
            'next_storage_backend': 'django.core.files.storage.FileSystemStorage',
            'next_storage_backend_arguments': {
                'location': self.document_storage_kwargs['location']
            }
        }

        self._call_command()

    def test_storage_processor_command_forwards(self):
        self._upload_and_call()

        with open(self.test_document.latest_version.file.path, mode='rb') as file_object:
            self.assertEqual(
                get_mimetype(file_object=file_object),
                ('application/zip', 'binary')
            )

        self.assertEqual(
            self.test_document.latest_version.checksum,
            self.test_document.latest_version.update_checksum(save=False)
        )

    def test_processor_forwards_and_reverse(self):
        self._upload_and_call()

        self._call_command(reverse=True)

        self.defined_storage.dotted_path = 'django.core.files.storage.FileSystemStorage'
        self.defined_storage.kwargs = {
            'location': self.document_storage_kwargs['location']
        }

        with open(self.test_document.latest_version.file.path, mode='rb') as file_object:
            self.assertNotEqual(
                get_mimetype(file_object=file_object),
                ('application/zip', 'binary')
            )

        self.assertEqual(
            self.test_document.latest_version.checksum,
            self.test_document.latest_version.update_checksum(save=False)
        )
