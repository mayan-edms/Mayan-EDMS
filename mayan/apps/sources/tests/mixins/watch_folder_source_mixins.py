import shutil

from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ...source_backends.literals import (
    DEFAULT_PERIOD_INTERVAL, SOURCE_UNCOMPRESS_CHOICE_NEVER
)
from ...source_backends.watch_folder_backends import SourceBackendWatchFolder

from .base_mixins import SourceTestMixin


class WatchFolderSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_watch_folder'

    def setUp(self):
        self._temporary_folders = []
        super().setUp()
        self.test_staging_folder_files = []

    def tearDown(self):
        for temporary_folders in self._temporary_folders:
            fs_cleanup(filename=temporary_folders)

        super().tearDown()

    def _create_test_watch_folder(self, extra_data=None):
        temporary_folder = mkdtemp()
        self._temporary_folders.append(temporary_folder)
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'folder_path': temporary_folder,
            'include_subdirectories': False,
            'interval': DEFAULT_PERIOD_INTERVAL,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendWatchFolder.get_class_path(),
            backend_data=backend_data
        )

    def _copy_test_watch_folder_document(self):
        shutil.copy(
            src=TEST_SMALL_DOCUMENT_PATH,
            dst=self.test_source.get_backend_data()['folder_path']
        )
