from mayan.apps.documents.tests.base import BaseTestCase

from .mixins import AssetTaskTestMixin, AssetTestMixin


class AssetTasksTestCase(AssetTaskTestMixin, AssetTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_asset()

    def test_asset_task_content_object_image_generate(self):
        self._execute_asset_task_content_object_image_generate()
