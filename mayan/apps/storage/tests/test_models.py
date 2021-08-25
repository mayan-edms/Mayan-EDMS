from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import DownloadFileTestMixin


class DownloadFileModelTestCase(DownloadFileTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_download_file()

        self.assertTrue(self.test_download_file.get_absolute_url())
