from django.core.files import File
from django.db.models import Q

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.permissions.tests.mixins import PermissionTestMixin

from ..classes import Layer
from ..models import Asset, LayerTransformation
from ..transformations import BaseTransformation

from .literals import (
    TEST_ASSET_LABEL, TEST_ASSET_LABEL_EDITED, TEST_ASSET_INTERNAL_NAME,
    TEST_ASSET_PATH, TEST_LAYER_LABEL, TEST_LAYER_ORDER, TEST_LAYER_NAME,
    TEST_TRANSFORMATION_ARGUMENT, TEST_TRANSFORMATION_ARGUMENT_EDITED,
    TEST_TRANSFORMATION_LABEL, TEST_TRANSFORMATION_NAME
)


class AssetAPIViewTestMixin:
    def _request_test_asset_create_api_view(self):
        pk_list = list(Asset.objects.values_list('pk', flat=True))

        with open(file=TEST_ASSET_PATH, mode='rb') as file_object:
            response = self.post(
                viewname='rest_api:asset-list', data={
                    'label': TEST_ASSET_LABEL,
                    'internal_name': TEST_ASSET_INTERNAL_NAME,
                    'file': File(file=file_object)
                }
            )

        try:
            self.test_asset = Asset.objects.get(~Q(pk__in=pk_list))
        except Asset.DoesNotExist:
            self.test_asset = None

        return response

    def _request_test_asset_delete_api_view(self):
        return self.delete(
            viewname='rest_api:asset-detail',
            kwargs={'asset_id': self.test_asset.pk}
        )

    def _request_test_asset_detail_api_view(self):
        return self.get(
            viewname='rest_api:asset-detail',
            kwargs={'asset_id': self.test_asset.pk}
        )

    def _request_test_asset_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:asset-detail', kwargs={
                'asset_id': self.test_asset.pk
            }, data={'label': TEST_ASSET_LABEL_EDITED}
        )

    def _request_test_asset_edit_via_put_api_view(self):
        with open(file=TEST_ASSET_PATH, mode='rb') as file_object:
            return self.put(
                viewname='rest_api:asset-detail', kwargs={
                    'asset_id': self.test_asset.pk
                }, data={
                    'label': TEST_ASSET_LABEL_EDITED,
                    'internal_name': TEST_ASSET_INTERNAL_NAME,
                    'file': File(file=file_object)
                }
            )

    def _request_test_asset_list_api_view(self):
        return self.get(viewname='rest_api:asset-list')


class AssetTestMixin:
    def _create_test_asset(self):
        with open(file=TEST_ASSET_PATH, mode='rb') as file_object:
            self.test_asset = Asset.objects.create(
                label=TEST_ASSET_LABEL,
                internal_name=TEST_ASSET_INTERNAL_NAME,
                file=File(file=file_object)
            )


class AssetViewTestMixin:
    def _request_test_asset_create_view(self):
        pk_list = list(Asset.objects.values_list('pk', flat=True))

        with open(file=TEST_ASSET_PATH, mode='rb') as file_object:
            response = self.post(
                viewname='converter:asset_create', data={
                    'label': TEST_ASSET_LABEL,
                    'internal_name': TEST_ASSET_INTERNAL_NAME,
                    'file': file_object
                }
            )

        self.test_asset = Asset.objects.exclude(
            pk__in=pk_list
        ).first()

        return response

    def _request_test_asset_delete_view(self):
        return self.post(
            viewname='converter:asset_single_delete', kwargs={
                'asset_id': self.test_asset.pk
            }
        )

    def _request_test_asset_detail_view(self):
        return self.get(
            viewname='converter:asset_detail', kwargs={
                'asset_id': self.test_asset.pk
            }
        )

    def _request_test_asset_edit_view(self):
        return self.post(
            viewname='converter:asset_edit', kwargs={
                'asset_id': self.test_asset.pk
            }, data={
                'label': TEST_ASSET_LABEL_EDITED,
                'internal_name': TEST_ASSET_INTERNAL_NAME,
            }
        )

    def _request_test_asset_list_view(self):
        return self.get(viewname='converter:asset_list')


class LayerTestCaseMixin:
    def setUp(self):
        super().setUp()
        Layer.invalidate_cache()


class LayerTestMixin(PermissionTestMixin):
    auto_create_test_layer = True

    def setUp(self):
        super().setUp()

        if self.auto_create_test_layer:
            self.test_layer = Layer(
                label=TEST_LAYER_LABEL, name=TEST_LAYER_NAME,
                order=TEST_LAYER_ORDER, permissions={}
            )

            self._create_test_permission()

            self.test_layer_permission = self.test_permission
            ModelPermission.register(
                model=self.test_document._meta.model, permissions=(
                    self.test_permission,
                )
            )

            self.test_layer.permissions = {
                'create': self.test_layer_permission,
                'delete': self.test_layer_permission,
                'edit': self.test_layer_permission,
                'select': self.test_layer_permission,
                'view': self.test_layer_permission,
            }

    def tearDown(self):
        if self.auto_create_test_layer:
            Layer._registry.pop(self.test_layer.name, None)

        super().tearDown()


class TransformationTestMixin(LayerTestMixin):
    auto_create_test_transformation_class = True

    def setUp(self):
        super().setUp()
        if self.auto_create_test_transformation_class:
            self._create_test_transformation_class()

        BaseTransformation.register(
            layer=self.test_layer, transformation=self.TestTransformationClass
        )

    def _create_test_transformation(self):
        self.test_transformation = self.test_layer.add_transformation_to(
            obj=self.test_document,
            transformation_class=self.TestTransformationClass,
            arguments=getattr(
                self, 'test_transformation_arguments',
                TEST_TRANSFORMATION_ARGUMENT
            )
        )

    def _create_test_transformation_class(self):
        class TestTransformation(BaseTransformation):
            arguments = ('test_argument',)
            label = TEST_TRANSFORMATION_LABEL
            name = TEST_TRANSFORMATION_NAME

            def execute_on(self, *args, **kwargs):
                super().execute_on(*args, **kwargs)

                return self.image

        self.TestTransformationClass = TestTransformation


class TransformationViewsTestMixin:
    def _request_transformation_create_post_view(self):
        pk_list = list(LayerTransformation.objects.values('pk'))

        response = self.post(
            viewname='converter:transformation_create', kwargs={
                'app_label': 'documents', 'model_name': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name,
                'transformation_name': self.TestTransformationClass.name,
            }, data={
                'arguments': getattr(
                    self, '.test_transformation_argument',
                    TEST_TRANSFORMATION_ARGUMENT
                )
            }
        )

        try:
            self.test_transformation = LayerTransformation.objects.get(
                ~Q(pk__in=pk_list)
            )
        except LayerTransformation.DoesNotExist:
            self.test_transformation = None

        return response

    def _request_transformation_create_get_view(self):
        return self.get(
            viewname='converter:transformation_create', kwargs={
                'app_label': 'documents', 'model_name': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name,
                'transformation_name': self.TestTransformationClass.name,
            }, data={
                'arguments': getattr(
                    self, '.test_transformation_argument',
                    TEST_TRANSFORMATION_ARGUMENT
                )
            }
        )

    def _request_transformation_delete_view(self):
        return self.post(
            viewname='converter:transformation_delete', kwargs={
                'layer_name': self.test_layer.name,
                'transformation_id': self.test_transformation.pk
            }
        )

    def _request_transformation_edit_view(self):
        return self.post(
            viewname='converter:transformation_edit', kwargs={
                'layer_name': self.test_layer.name,
                'transformation_id': self.test_transformation.pk
            }, data={
                'arguments': getattr(
                    self, 'test_transformation_argument_edited',
                    TEST_TRANSFORMATION_ARGUMENT_EDITED
                )
            }
        )

    def _request_transformation_list_view(self):
        return self.get(
            viewname='converter:transformation_list', kwargs={
                'app_label': 'documents', 'model_name': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name
            }
        )

    def _request_test_transformation_select_get_view(self):
        return self.get(
            viewname='converter:transformation_select', kwargs={
                'app_label': 'documents', 'model_name': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name
            }
        )

    def _request_test_transformation_select_post_view(self):
        return self.post(
            viewname='converter:transformation_select', kwargs={
                'app_label': 'documents', 'model_name': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name
            }, data={
                'transformation': self.TestTransformationClass.name
            }
        )
