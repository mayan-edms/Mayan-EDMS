import shutil

from mayan.apps.storage.utils import mkdtemp

from ...source_backends.literals import (
    DEFAULT_PERIOD_INTERVAL, SOURCE_UNCOMPRESS_CHOICE_NEVER
)
from ...source_backends.watch_folder_backends import SourceBackendWatchFolder

from .base_mixins import SourceTestMixin


class WatchFolderTestMixin(SourceTestMixin):
    def setUp(self):
        super().setUp()
        self.temporary_directory = mkdtemp()
        self.test_watch_folders = []

    def tearDown(self):
        shutil.rmtree(path=self.temporary_directory)
        super().tearDown()

    def _create_test_watchfolder(self, extra_data=None):
        backend_data = {
            'document_type_id': self.test_document_type.pk,
            'folder_path': self.temporary_directory,
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
