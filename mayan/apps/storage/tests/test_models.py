from mayan.apps.events.classes import EventModelRegistry
from mayan.apps.testing.tests.base import BaseTestCase

from ..models import DownloadFile, SharedUploadedFile
from ..settings import (
    setting_download_file_expiration_interval,
    setting_shared_uploaded_file_expiration_interval
)

from .mixins import DownloadFileTestMixin, SharedUploadedFileTestMixin


class DownloadFileModelTestCase(DownloadFileTestMixin, BaseTestCase):
    def test_download_file_expiration(self):
        setting_download_file_expiration_interval.set(value=60)
        self._create_test_download_file()

        self.assertEqual(DownloadFile.objects.stale().count(), 0)

        setting_download_file_expiration_interval.set(value=0)

        self.assertEqual(DownloadFile.objects.stale().count(), 1)

    def test_method_get_absolute_url_without_content_object(self):
        self._create_test_download_file()

        self.assertFalse(self.test_download_file.get_absolute_url())

    def test_method_get_absolute_url_with_content_object(self):
        self._create_test_object()
        self.TestModel.add_to_class(
            name='get_absolute_url', value=lambda self: 'test_value'
        )
        EventModelRegistry.register(model=self.TestModel)

        self._create_test_download_file(content_object=self.test_object)

        self.assertTrue(self.test_download_file.get_absolute_url())


class SharedUploadedFileManagerTestCase(
    SharedUploadedFileTestMixin, BaseTestCase
):
    def test_shared_uploaded_expiration(self):
        setting_shared_uploaded_file_expiration_interval.set(value=60)
        self._create_test_shared_uploaded_file()

        self.assertEqual(SharedUploadedFile.objects.stale().count(), 0)

        setting_shared_uploaded_file_expiration_interval.set(value=0)

        self.assertEqual(SharedUploadedFile.objects.stale().count(), 1)
