from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.tests.tests.base import GenericViewTestCase

from ..models import LayerTransformation

from .mixins import (
    AssetTestMixin, AssetViewTestMixin, TransformationTestMixin,
    TransformationViewsTestMixin
)

from ..models import Asset
from ..permissions import (
    permission_asset_create, permission_asset_delete,
    permission_asset_edit, permission_asset_view,
)


class AssetViewTestCase(
    AssetTestMixin, AssetViewTestMixin, GenericViewTestCase
):
    def test_asset_create_view_no_permissions(self):
        asset_count = Asset.objects.count()

        response = self._request_test_asset_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Asset.objects.count(), asset_count)

    def test_asset_create_view_with_permissions(self):
        self.grant_permission(permission=permission_asset_create)

        asset_count = Asset.objects.count()

        response = self._request_test_asset_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Asset.objects.count(), asset_count + 1)

    def test_asset_delete_view_no_permissions(self):
        self._create_test_asset()

        asset_count = Asset.objects.count()

        response = self._request_test_asset_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Asset.objects.count(), asset_count)

    def test_asset_delete_view_with_access(self):
        self._create_test_asset()

        self.grant_access(
            obj=self.test_asset, permission=permission_asset_delete
        )

        asset_count = Asset.objects.count()

        response = self._request_test_asset_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Asset.objects.count(), asset_count - 1)

    def test_asset_edit_view_no_permissions(self):
        self._create_test_asset()

        asset_label = self.test_asset.label

        response = self._request_test_asset_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_asset.refresh_from_db()
        self.assertEqual(self.test_asset.label, asset_label)

    def test_asset_edit_view_with_access(self):
        self._create_test_asset()

        self.grant_access(
            obj=self.test_asset, permission=permission_asset_edit
        )

        asset_label = self.test_asset.label

        response = self._request_test_asset_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_asset.refresh_from_db()
        self.assertNotEqual(self.test_asset.label, asset_label)

    def test_asset_list_view_with_no_permission(self):
        self._create_test_asset()

        response = self._request_test_asset_list_view()
        self.assertNotContains(
            response=response, text=self.test_asset.label, status_code=200
        )

    def test_asset_list_view_with_access(self):
        self._create_test_asset()

        self.grant_access(obj=self.test_asset, permission=permission_asset_view)

        response = self._request_test_asset_list_view()
        self.assertContains(
            response=response, text=self.test_asset.label, status_code=200
        )


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

    def test_transformation_select_get_view_no_permission(self):
        self._create_test_transformation_class()
        transformation_count = LayerTransformation.objects.count()

        response = self._request_test_transformation_select_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

    def test_transformation_select_get_view_with_access(self):
        self._create_test_transformation_class()
        self.grant_access(
            obj=self.test_document, permission=self.test_permission
        )
        transformation_count = LayerTransformation.objects.count()

        response = self._request_test_transformation_select_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

    def test_transformation_select_post_view_no_permission(self):
        self._create_test_transformation_class()
        transformation_count = LayerTransformation.objects.count()

        response = self._request_test_transformation_select_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

    def test_transformation_select_post_view_with_access(self):
        self._create_test_transformation_class()
        self.grant_access(
            obj=self.test_document, permission=self.test_permission
        )
        transformation_count = LayerTransformation.objects.count()

        response = self._request_test_transformation_select_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )
