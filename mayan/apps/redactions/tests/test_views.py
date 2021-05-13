from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.tests.mixins import (
    TransformationTestMixin, TransformationViewsTestMixin
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..layers import layer_redactions
from ..transformations import TransformationRedactionPercent

from .literals import (
    TEST_REDACTION_ARGUMENT, TEST_REDACTION_ARGUMENT_EDITED
)


class RedactionViewsTestCase(
    TransformationTestMixin, TransformationViewsTestMixin,
    GenericDocumentViewTestCase
):
    auto_create_test_layer = False
    auto_create_test_transformation_class = False
    test_layer = layer_redactions
    test_transformation_argument = TEST_REDACTION_ARGUMENT
    test_transformation_argument_edited = TEST_REDACTION_ARGUMENT_EDITED
    TestTransformationClass = TransformationRedactionPercent

    def test_redaction_create_post_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_create_post_view_with_permission(self):
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['create']
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_create_get_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_create_get_view_with_permission(self):
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['create']
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_delete_view_no_permission(self):
        self._create_test_transformation()
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_delete_view_with_access(self):
        self._create_test_transformation()
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['delete']
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_edit_view_no_permission(self):
        self._create_test_transformation()
        transformation_arguments = self.test_transformation.arguments

        self._clear_events()

        response = self._request_transformation_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_transformation.refresh_from_db()
        self.assertEqual(
            transformation_arguments, self.test_transformation.arguments
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_edit_view_with_access(self):
        self._create_test_transformation()
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['edit']
        )
        transformation_arguments = self.test_transformation.arguments

        self._clear_events()

        response = self._request_transformation_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_transformation.refresh_from_db()
        self.assertNotEqual(
            transformation_arguments, self.test_transformation.arguments
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_list_view_no_permission(self):
        self._create_test_transformation()

        self._clear_events()

        response = self._request_transformation_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response=response,
            text=self.test_transformation.get_transformation_class().label,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_list_view_with_access(self):
        self._create_test_transformation()
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['view']
        )

        self._clear_events()

        response = self._request_transformation_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response=response,
            text=self.test_transformation.get_transformation_class().label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_get_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_get_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['select']
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_post_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_post_view_with_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=self.test_layer.permissions['select']
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
