import mock

from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.file_caching.models import CachePartition

from .mixins import AssetTestMixin


class AssetModelTestCase(
    AssetTestMixin, BaseTestCase
):
    def test_asset_get_absolute_url_method(self):
        self._create_test_asset()

        self.test_asset.get_absolute_url()

    def test_asset_generate_image_method(self):
        self._create_test_asset()

        with mock.patch.object(CachePartition, attribute='create_file') as mock_cache_partition_create_file:
            self.test_asset.generate_image()
            self.assertTrue(mock_cache_partition_create_file.called)

        self.test_asset.generate_image()

        with mock.patch.object(CachePartition, attribute='create_file') as mock_cache_partition_create_file:
            self.test_asset.generate_image()
            self.assertFalse(mock_cache_partition_create_file.called)
