from io import BytesIO

from PIL import Image

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.transformations import TransformationRotate270
from mayan.apps.documents.permissions import permission_document_file_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin

from .literals import TEST_REDACTION_DOCUMENT_PATH
from .mixins import LayerMaximumOrderAPIViewTestMixin


class LayerMaximumOrderAPIViewTestCase(
    LayerMaximumOrderAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    test_document_path = TEST_REDACTION_DOCUMENT_PATH

    def test_redaction_maximum_layer_order(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        layer_saved_transformations.add_transformation_to(
            obj=self.test_document_file_page,
            transformation_class=TransformationRotate270
        )

        self._clear_events()

        response = self._request_document_file_page_image_api_view_with_maximum_layer_order()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        image_buffer = BytesIO(response.content)
        image = Image.open(fp=image_buffer)

        self.assertEqual(image.getpixel(xy=(0, 0)), (0, 0, 0))

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
