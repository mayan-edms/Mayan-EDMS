from django.test import TestCase

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..transformations import (
    BaseTransformation, TransformationCrop, TransformationLineArt,
    TransformationResize, TransformationRotate, TransformationRotate90,
    TransformationRotate180, TransformationRotate270, TransformationZoom
)

from .literals import (
    TEST_TRANSFORMATION_COMBINED_CACHE_HASH,
    TEST_TRANSFORMATION_RESIZE_CACHE_HASH,
    TEST_TRANSFORMATION_RESIZE_CACHE_HASH_2,
    TEST_TRANSFORMATION_RESIZE_HEIGHT, TEST_TRANSFORMATION_RESIZE_HEIGHT_2,
    TEST_TRANSFORMATION_RESIZE_WIDTH, TEST_TRANSFORMATION_RESIZE_WIDTH_2,
    TEST_TRANSFORMATION_ROTATE_CACHE_HASH,
    TEST_TRANSFORMATION_ROTATE_DEGRESS, TEST_TRANSFORMATION_ZOOM_CACHE_HASH,
    TEST_TRANSFORMATION_ZOOM_PERCENT
)
from .mixins import LayerTestMixin


class TransformationBaseTestCase(TestCase):
    def test_cache_uniqness(self):
        transformation_1 = TransformationResize(width=640, height=640)

        transformation_2 = TransformationResize(width=800, height=800)

        self.assertNotEqual(
            transformation_1.cache_hash(), transformation_2.cache_hash()
        )

    def test_cache_combining_uniqness(self):
        transformation_1 = TransformationZoom(percent=100)
        transformation_2 = TransformationResize(width=800, height=800)

        self.assertNotEqual(
            BaseTransformation.combine((transformation_1, transformation_2)),
            BaseTransformation.combine((transformation_2, transformation_1)),
        )

    def test_resize_cache_hashing(self):
        # Test if the hash is being generated correctly
        transformation = TransformationResize(
            width=TEST_TRANSFORMATION_RESIZE_WIDTH,
            height=TEST_TRANSFORMATION_RESIZE_HEIGHT
        )

        self.assertEqual(
            transformation.cache_hash(), TEST_TRANSFORMATION_RESIZE_CACHE_HASH
        )

        # Test if the hash is being alternated correctly
        transformation = TransformationResize(
            width=TEST_TRANSFORMATION_RESIZE_WIDTH_2,
            height=TEST_TRANSFORMATION_RESIZE_HEIGHT_2
        )

        self.assertEqual(
            transformation.cache_hash(),
            TEST_TRANSFORMATION_RESIZE_CACHE_HASH_2
        )

    def test_rotate_cache_hashing(self):
        # Test if the hash is being generated correctly
        transformation = TransformationRotate(
            degrees=TEST_TRANSFORMATION_ROTATE_DEGRESS
        )

        self.assertEqual(
            transformation.cache_hash(), TEST_TRANSFORMATION_ROTATE_CACHE_HASH
        )

    def test_rotate_zoom_hashing(self):
        # Test if the hash is being generated correctly
        transformation = TransformationZoom(
            percent=TEST_TRANSFORMATION_ZOOM_PERCENT
        )

        self.assertEqual(
            transformation.cache_hash(), TEST_TRANSFORMATION_ZOOM_CACHE_HASH
        )

    def test_cache_hash_combining(self):
        # Test magic method and hash combining

        transformation_resize = TransformationResize(
            width=TEST_TRANSFORMATION_RESIZE_WIDTH,
            height=TEST_TRANSFORMATION_RESIZE_HEIGHT
        )

        transformation_rotate = TransformationRotate(
            degrees=TEST_TRANSFORMATION_ROTATE_DEGRESS
        )

        transformation_zoom = TransformationZoom(
            percent=TEST_TRANSFORMATION_ZOOM_PERCENT
        )

        self.assertEqual(
            BaseTransformation.combine(
                (
                    transformation_rotate, transformation_resize,
                    transformation_zoom
                )
            ), TEST_TRANSFORMATION_COMBINED_CACHE_HASH
        )


class TransformationTestCase(LayerTestMixin, GenericDocumentTestCase):
    auto_create_test_transformation_class = False

    def test_crop_transformation_optional_arguments(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationCrop
        )

        self._silence_logger(name='mayan.apps.converter.managers')

        document_page = self.test_document.pages.first()

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationCrop,
            arguments={'top': '10'}
        )

        self.assertTrue(document_page.generate_image())

    def test_crop_transformation_invalid_arguments(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationCrop
        )

        self._silence_logger(name='mayan.apps.converter.managers')

        document_page = self.test_document.pages.first()

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationCrop,
            arguments={'top': 'x', 'left': '-'}
        )
        self.assertTrue(document_page.generate_image())

    def test_crop_transformation_non_valid_range_arguments(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationCrop
        )

        self._silence_logger(name='mayan.apps.converter.managers')

        document_page = self.test_document.pages.first()

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationCrop,
            arguments={'top': '-1000', 'bottom': '100000000'}
        )

        self.assertTrue(document_page.generate_image())

    def test_crop_transformation_overlapping_ranges_arguments(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationCrop
        )

        self._silence_logger(name='mayan.apps.converter.managers')

        document_page = self.test_document.pages.first()

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationCrop,
            arguments={'top': '1000', 'bottom': '1000'}
        )

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationCrop,
            arguments={'left': '1000', 'right': '10000'}
        )

        self.assertTrue(document_page.generate_image())

    def test_lineart_transformations(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationLineArt
        )

        document_page = self.test_document.pages.first()

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationLineArt,
            arguments={}
        )

        self.assertTrue(document_page.generate_image())

    def test_rotate_transformations(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationRotate90
        )

        document_page = self.test_document.pages.first()

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationRotate90,
            arguments={}
        )

        self.assertTrue(document_page.generate_image())

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationRotate180,
            arguments={}
        )

        self.assertTrue(document_page.generate_image())

        self.test_layer.add_transformation_to(
            obj=document_page, transformation_class=TransformationRotate270,
            arguments={}
        )

        self.assertTrue(document_page.generate_image())
