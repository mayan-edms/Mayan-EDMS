from pathlib import Path
import shutil

from django.utils.encoding import force_text

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.mimetype.api import get_mimetype

from ..utils import PassthroughStorageProcessor, mkdtemp, patch_files

from .mixins import StorageProcessorTestMixin


class PatchFilesTestCase(BaseTestCase):
    test_replace_text = 'replaced_text'

    def setUp(self):
        super(PatchFilesTestCase, self).setUp()
        self.temporary_directory = mkdtemp()
        self.path_temporary_directory = Path(self.temporary_directory)
        self.path_test_file = self.path_temporary_directory / 'test_file.txt'

        with self.path_test_file.open(mode='w') as file_object:
            file_object.writelines(
                [
                    'line 1\n',
                    '    line 2\n',
                    'line 3\n',
                ]
            )

    def tearDown(self):
        super(PatchFilesTestCase, self).tearDown()
        shutil.rmtree(path=self.temporary_directory, ignore_errors=True)

    def _patch_test_file(self):
        replace_list = [
            {
                'filename_pattern': '*',
                'content_patterns': [
                    {
                        'search': self.test_search_text,
                        'replace': self.test_replace_text,
                    }
                ]
            }
        ]
        patch_files(
            path=self.path_temporary_directory, replace_list=replace_list
        )

        with self.path_test_file.open(mode='r') as file_object:
            self.final_text = file_object.read()

    def test_file_patching_single_line(self):
        self.test_search_text = 'line 1'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'replaced_text\n    line 2\nline 3\n')

    def test_file_patching_multi_line(self):
        self.test_search_text = 'line 2\nline 3\n'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'line 1\n    replaced_text')

    def test_file_patching_spaces(self):
        self.test_search_text = '    line 2'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'line 1\nreplaced_text\nline 3\n')

    def test_file_patching_no_matches(self):
        self.test_search_text = 'line 4'

        self._patch_test_file()

        self.assertEqual(self.final_text, 'line 1\n    line 2\nline 3\n')


class StorageProcessorTestCase(
    StorageProcessorTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def _execute_storage_procesor(self, reverse=None):
        storage_processor = PassthroughStorageProcessor(
            app_label='documents',
            defined_storage_name='documents__documentversion',
            log_file=force_text(s=self.path_test_file),
            model_name='DocumentVersion'
        )
        storage_processor.execute(reverse=reverse)

    def _upload_and_process(self):
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

        self._execute_storage_procesor()

    def test_processor_forwards(self):
        self._upload_and_process()

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
        self._upload_and_process()

        self._execute_storage_procesor(reverse=True)

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
