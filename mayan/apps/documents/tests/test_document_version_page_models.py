from mayan.apps.converter.transformations import (
    BaseTransformation, TransformationRotate90
)
from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.tests.mixins import LayerTestMixin

from ..literals import DOCUMENT_FILE_ACTION_PAGES_APPEND

from .base import GenericDocumentTestCase


class DocumentVersionPageTestCase(LayerTestMixin, GenericDocumentTestCase):
    def _get_test_document_version_page_cached_image(self):
        cache_file = self.test_document_version_page.cache_partition.get_file(
            filename=self.test_document_version_page.get_combined_cache_filename()
        )
        with cache_file.open() as file_object:
            return file_object.read()

    def test_version_pages_reset_no_file(self):
        self.test_document_file.delete()
        self.test_document_version.pages_reset()

    def test_version_pages_reset(self):
        self._upload_test_document_file(action=DOCUMENT_FILE_ACTION_PAGES_APPEND)

        test_document_version_page_content_objects = self.test_document.versions.last().page_content_objects

        self.test_document_version.pages_reset()

        self.assertNotEqual(
            self.test_document.versions.last().page_content_objects,
            test_document_version_page_content_objects
        )
        self.assertEqual(
            self.test_document.versions.last().page_content_objects,
            list(self.test_document.file_latest.pages.all())
        )

    def test_method_get_absolute_url(self):
        self.assertTrue(
            self.test_document.version_active.pages.first().get_absolute_url()
        )

    def test_version_page_cache_update_on_transformation(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationRotate90
        )

        test_combined_cache_filename_1 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_1 = self.test_document_version_page.generate_image()
        test_api_image_url_1 = self.test_document_version_page.get_api_image_url()
        test_image_1 = self._get_test_document_version_page_cached_image()

        self.test_layer.add_transformation_to(
            obj=self.test_document_version_page,
            transformation_class=TransformationRotate90, arguments={}
        )

        test_combined_cache_filename_2 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_2 = self.test_document_version_page.generate_image()
        test_api_image_url_2 = self.test_document_version_page.get_api_image_url()
        test_image_2 = self._get_test_document_version_page_cached_image()

        self.assertNotEqual(test_combined_cache_filename_1, test_combined_cache_filename_2)
        self.assertNotEqual(test_generate_image_1, test_generate_image_2)
        self.assertNotEqual(test_api_image_url_1, test_api_image_url_2)
        self.assertNotEqual(test_image_1, test_image_2)

    def test_version_page_cache_update_on_source_transformation(self):
        BaseTransformation.register(
            layer=self.test_layer, transformation=TransformationRotate90
        )

        test_document_version_page_content_object = self.test_document_version_page.content_object

        # Original.
        test_combined_cache_filename_1 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_1 = self.test_document_version_page.generate_image()
        test_api_image_url_1 = self.test_document_version_page.get_api_image_url()
        # Source is at 0 deg, version is at 0 deg = image is at 0 deg.
        test_image_1 = self._get_test_document_version_page_cached_image()

        # Add transformation to content object.
        self.test_layer.add_transformation_to(
            obj=test_document_version_page_content_object,
            transformation_class=TransformationRotate90, arguments={}
        )

        test_combined_cache_filename_2 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_2 = self.test_document_version_page.generate_image()
        test_api_image_url_2 = self.test_document_version_page.get_api_image_url()
        # Source is at 90 deg, version is at 0 deg = image is at 90 deg.
        test_image_2 = self._get_test_document_version_page_cached_image()

        self.assertNotEqual(test_combined_cache_filename_1, test_combined_cache_filename_2)
        self.assertNotEqual(test_generate_image_1, test_generate_image_2)
        self.assertNotEqual(test_api_image_url_1, test_api_image_url_2)
        self.assertNotEqual(test_image_1, test_image_2)

        # Add transformation to document version page.
        self.test_layer.add_transformation_to(
            obj=self.test_document_version_page,
            transformation_class=TransformationRotate90, arguments={}
        )

        test_combined_cache_filename_3 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_3 = self.test_document_version_page.generate_image()
        test_api_image_url_3 = self.test_document_version_page.get_api_image_url()
        # Source is at 90 deg, version is at 90 deg = image is at 180 deg.
        test_image_3 = self._get_test_document_version_page_cached_image()

        self.assertNotEqual(test_combined_cache_filename_2, test_combined_cache_filename_3)
        self.assertNotEqual(test_generate_image_2, test_generate_image_3)
        self.assertNotEqual(test_api_image_url_2, test_api_image_url_3)
        self.assertNotEqual(test_image_2, test_image_3)

        self.assertNotEqual(test_combined_cache_filename_1, test_combined_cache_filename_3)
        self.assertNotEqual(test_generate_image_1, test_generate_image_3)
        self.assertNotEqual(test_api_image_url_1, test_api_image_url_3)
        self.assertNotEqual(test_image_1, test_image_3)

        # Remove transformation from document content object.
        LayerTransformation.objects.get_for_object(
            obj=test_document_version_page_content_object
        ).delete()

        test_combined_cache_filename_4 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_4 = self.test_document_version_page.generate_image()
        test_api_image_url_4 = self.test_document_version_page.get_api_image_url()
        # Source is at 0 deg, version is at 90 deg = image is at 90 deg.
        test_image_4 = self._get_test_document_version_page_cached_image()

        self.assertNotEqual(test_combined_cache_filename_1, test_combined_cache_filename_4)
        self.assertNotEqual(test_generate_image_1, test_generate_image_4)
        self.assertNotEqual(test_api_image_url_1, test_api_image_url_4)
        self.assertNotEqual(test_image_1, test_image_4)

        self.assertNotEqual(test_combined_cache_filename_2, test_combined_cache_filename_4)
        self.assertNotEqual(test_generate_image_2, test_generate_image_4)
        self.assertEqual(test_api_image_url_2, test_api_image_url_4)
        # Image 2 and 4 are equal

        self.assertNotEqual(test_combined_cache_filename_3, test_combined_cache_filename_4)
        self.assertNotEqual(test_generate_image_3, test_generate_image_4)
        self.assertNotEqual(test_api_image_url_3, test_api_image_url_4)
        self.assertNotEqual(test_image_3, test_image_4)

        # Remove transformation from document version page.
        LayerTransformation.objects.get_for_object(
            obj=self.test_document_version_page
        ).delete()

        test_combined_cache_filename_5 = self.test_document_version_page.get_combined_cache_filename()
        test_generate_image_5 = self.test_document_version_page.generate_image()
        test_api_image_url_5 = self.test_document_version_page.get_api_image_url()
        # Source is at 0 deg, version is at 0 deg = image is at 0 deg.
        test_image_5 = self._get_test_document_version_page_cached_image()

        self.assertEqual(test_combined_cache_filename_1, test_combined_cache_filename_5)
        self.assertEqual(test_generate_image_1, test_generate_image_5)
        self.assertEqual(test_api_image_url_1, test_api_image_url_5)
        self.assertEqual(test_image_1, test_image_5)

        self.assertNotEqual(test_combined_cache_filename_2, test_combined_cache_filename_5)
        self.assertNotEqual(test_generate_image_2, test_generate_image_5)
        self.assertNotEqual(test_api_image_url_2, test_api_image_url_5)
        self.assertNotEqual(test_image_2, test_image_5)

        self.assertNotEqual(test_combined_cache_filename_3, test_combined_cache_filename_5)
        self.assertNotEqual(test_generate_image_3, test_generate_image_5)
        self.assertNotEqual(test_api_image_url_3, test_api_image_url_5)
        self.assertNotEqual(test_image_3, test_image_5)

        self.assertNotEqual(test_combined_cache_filename_4, test_combined_cache_filename_5)
        self.assertNotEqual(test_generate_image_4, test_generate_image_5)
        self.assertNotEqual(test_api_image_url_4, test_api_image_url_5)
        self.assertNotEqual(test_image_4, test_image_5)

        self.assertEqual(test_combined_cache_filename_1, test_combined_cache_filename_5)
        self.assertEqual(test_generate_image_1, test_generate_image_5)
        self.assertEqual(test_api_image_url_1, test_api_image_url_5)
        self.assertEqual(test_image_1, test_image_5)
