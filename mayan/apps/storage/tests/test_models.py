from mayan.apps.events.classes import EventModelRegistry
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import DownloadFileTestMixin


class DownloadFileModelTestCase(DownloadFileTestMixin, BaseTestCase):
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
