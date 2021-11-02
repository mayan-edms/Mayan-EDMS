from PIL import Image

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..layers import layer_decorations
from ..transformations import TransformationAssetPastePercent

from .mixins import AssetTestMixin


class DecorationTestCase(AssetTestMixin, GenericDocumentTestCase):
    auto_create_test_transformation_class = False

    def _get_test_document_version_page_image(self):
        cache_filename = self.test_document_version_page.generate_image()
        cache_file = self.test_document_version_page.cache_partition.get_file(
            filename=cache_filename
        )
        with cache_file.open() as file_object:
            image = Image.open(fp=file_object)
            image.load()
            return image

    def test_asset_paste_percent_transformation(self):
        self._create_test_asset()

        test_asset_pixel_color = self.test_asset.get_image().getpixel(
            xy=(0, 0)
        )[0:3]

        test_document_version_page_image = self._get_test_document_version_page_image()
        self.assertNotEqual(
            test_document_version_page_image.getpixel(xy=(0, 0)),
            test_asset_pixel_color
        )

        self.assertNotEqual(
            test_document_version_page_image.getpixel(
                xy=(
                    test_document_version_page_image.size[0] / 2,
                    test_document_version_page_image.size[1] / 2
                )
            ), test_asset_pixel_color
        )

        layer_decorations.add_transformation_to(
            obj=self.test_document_version_page,
            transformation_class=TransformationAssetPastePercent,
            arguments={
                'asset_name': self.test_asset.internal_name,
                'left': 50,
                'top': 50
            }
        )

        transformations = layer_decorations.get_transformations_for(
            as_classes=True, obj=self.test_document_version_page
        )

        test_asset_images = transformations[0].get_asset_images()
        position_x = test_asset_images['image_asset'].size[0] / 2
        position_y = test_asset_images['image_asset'].size[1] / 2

        test_document_version_page_image = self._get_test_document_version_page_image()

        self.assertNotEqual(
            test_document_version_page_image.getpixel(
                xy=(position_x, position_y)
            ), test_asset_pixel_color
        )

        self.assertEqual(
            test_document_version_page_image.getpixel(
                xy=(
                    test_document_version_page_image.size[0] / 2,
                    test_document_version_page_image.size[1] / 2
                )
            ), test_asset_pixel_color
        )
