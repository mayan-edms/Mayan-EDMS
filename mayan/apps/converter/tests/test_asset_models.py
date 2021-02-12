from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import AssetTestMixin


class AssetModelTestCase(
    AssetTestMixin, BaseTestCase
):
    def test_asset_get_absolute_url_method(self):
        self._create_test_asset()

        self.test_asset.get_absolute_url()
