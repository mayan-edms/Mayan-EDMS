from io import BytesIO

from PIL import Image

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.tests.literals import TEST_TRANSFORMATION_DOCUMENT_PATH
from mayan.apps.converter.transformations import TransformationRotate270
from mayan.apps.documents.tests.mixins.document_file_mixins import DocumentFilePageAPIViewTestMixin
from mayan.apps.documents.permissions import permission_document_file_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin

from ..layers import layer_redactions
from ..transformations import TransformationRedactionPercent
from ..permissions import permission_redaction_exclude


class LayerMaximumOrderAPIViewTestCase(
    DocumentFilePageAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    test_document_path = TEST_TRANSFORMATION_DOCUMENT_PATH

    def test_redaction_maximum_layer_order_exclude_transformation(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        layer_saved_transformations.add_transformation_to(
            obj=self.test_document_file_page,
            transformation_class=TransformationRotate270
        )

        self._clear_events()

        response = self._request_test_document_file_page_image_api_view(
            maximum_layer_order=layer_redactions.order
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        image_buffer = BytesIO(b''.join(response.streaming_content))
        image = Image.open(fp=image_buffer)

        self.assertEqual(image.getpixel(xy=(0, 0)), (254, 0, 0))

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_image_request_with_layer_below_redaction_no_permission(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        layer_redactions.add_transformation_to(
            obj=self.test_document_file_page,
            transformation_class=TransformationRedactionPercent(
                left=0, top=0, right=95, bottom=95
            )
        )

        self._clear_events()

        response = self._request_test_document_file_page_image_api_view(
            maximum_layer_order=layer_redactions.order - 1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        image_buffer = BytesIO(b''.join(response.streaming_content))
        image = Image.open(fp=image_buffer)

        self.assertEqual(image.getpixel(xy=(0, 0)), (0, 0, 0))

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_image_request_with_layer_below_redaction_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_redaction_exclude
        )

        layer_redactions.add_transformation_to(
            obj=self.test_document_file_page,
            transformation_class=TransformationRedactionPercent(
                left=0, top=0, right=95, bottom=95
            )
        )

        self._clear_events()

        response = self._request_test_document_file_page_image_api_view(
            maximum_layer_order=layer_redactions.order - 1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        image_buffer = BytesIO(b''.join(response.streaming_content))
        image = Image.open(fp=image_buffer)

        self.assertEqual(image.getpixel(xy=(0, 0)), (254, 0, 0))

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
