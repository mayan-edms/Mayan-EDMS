from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import LayerTransformation

from .mixins import TransformationTestMixin, TransformationViewsTestMixin


class TransformationViewsTestCase(
    TransformationTestMixin, TransformationViewsTestMixin,
    GenericDocumentViewTestCase
):
    def test_transformation_create_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        response = self._request_transformation_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

    def test_transformation_create_view_with_permission(self):
        self.grant_access(
            obj=self.test_document, permission=self.test_permission
        )

        transformation_count = LayerTransformation.objects.count()

        response = self._request_transformation_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count + 1
        )

    def test_transformation_delete_view_no_permission(self):
        self._create_test_transformation()

        transformation_count = LayerTransformation.objects.count()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

    def test_transformation_delete_view_with_access(self):
        self._create_test_transformation()

        self.grant_access(
            obj=self.test_document, permission=self.test_layer_permission
        )

        transformation_count = LayerTransformation.objects.count()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count - 1
        )

    def test_transformation_edit_view_no_permission(self):
        self._create_test_transformation()

        transformation_arguments = self.test_transformation.arguments

        response = self._request_transformation_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_transformation.refresh_from_db()
        self.assertEqual(
            transformation_arguments, self.test_transformation.arguments
        )

    def test_transformation_edit_view_with_access(self):
        self._create_test_transformation()

        self.grant_access(
            obj=self.test_document, permission=self.test_layer_permission
        )

        transformation_arguments = self.test_transformation.arguments
        response = self._request_transformation_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_transformation.refresh_from_db()
        self.assertNotEqual(
            transformation_arguments, self.test_transformation.arguments
        )

    def test_transformation_list_view_no_permission(self):
        self._create_test_transformation()

        response = self._request_transformation_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response=response,
            text=self.test_transformation.get_transformation_class().label,
            status_code=404
        )

    def test_transformation_list_view_with_access(self):
        self._create_test_transformation()

        self.grant_access(
            obj=self.test_document, permission=self.test_permission
        )

        response = self._request_transformation_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response=response,
            text=self.test_transformation.get_transformation_class().label,
            status_code=200
        )
