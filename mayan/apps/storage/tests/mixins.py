from pathlib import Path
import shutil

from mayan.apps.documents.literals import STORAGE_NAME_DOCUMENT_VERSION

from ..classes import DefinedStorage
from ..utils import mkdtemp


class StorageProcessorTestMixin:
    @classmethod
    def setUpClass(cls):
        super(StorageProcessorTestMixin, cls).setUpClass()
        cls.defined_storage = DefinedStorage.get(
            name=STORAGE_NAME_DOCUMENT_VERSION
        )
        cls.document_storage_kwargs = cls.defined_storage.kwargs

    def setUp(self):
        super(StorageProcessorTestMixin, self).setUp()
        self.temporary_directory = mkdtemp()
        self.path_temporary_directory = Path(self.temporary_directory)
        self.path_test_file = self.path_temporary_directory / 'test_file.txt'

    def tearDown(self):
        super(StorageProcessorTestMixin, self).tearDown()
        shutil.rmtree(path=self.temporary_directory, ignore_errors=True)
        self.defined_storage.kwargs = self.document_storage_kwargs
