from django.contrib.contenttypes.models import ContentType

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.permissions.tests.mixins import PermissionTestMixin

from ..classes import Layer
from ..models import ObjectLayer
from ..transformations import BaseTransformation

from .literals import (
    TEST_TRANSFORMATION_CLASS_LABEL, TEST_TRANSFORMATION_CLASS_NAME,
    TEST_TRANSFORMATION_NAME, TEST_TRANSFORMATION_ARGUMENT,
    TEST_TRANSFORMATION_ARGUMENT_EDITED
)


class LayerTestCaseMixin(object):
    def setUp(self):
        super(LayerTestCaseMixin, self).setUp()
        Layer.invalidate_cache()


class LayerTestMixin(PermissionTestMixin):
    test_layer = Layer(
        label='Test layer', name='test_layer', order=1000,
        permissions={}
    )

    def setUp(self):
        super(LayerTestMixin, self).setUp()
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


class TransformationTestMixin(LayerTestMixin):
    def _create_test_transformation(self):
        content_type = ContentType.objects.get_for_model(
            model=self.test_document
        )
        object_layer, created = ObjectLayer.objects.get_or_create(
            content_type=content_type, object_id=self.test_document.pk,
            stored_layer=self.test_layer.stored_layer
        )

        self.test_transformation = object_layer.transformations.create(
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

    def _create_test_transformation_class(self):
        class TestTransformation(BaseTransformation):
            arguments = ('test_argument',)
            label = TEST_TRANSFORMATION_CLASS_LABEL
            name = TEST_TRANSFORMATION_CLASS_NAME

            def execute_on(self, *args, **kwargs):
                super(TestTransformation, self).execute_on(*args, **kwargs)

                return self.image

        BaseTransformation.register(
            layer=self.test_layer, transformation=TestTransformation
        )

        self.TestTransformationClass = TestTransformation


class TransformationViewsTestMixin(object):
    def _request_transformation_create_view(self):
        return self.post(
            viewname='converter:transformation_create', kwargs={
                'app_label': 'documents', 'model_name': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name,
                'transformation_name': TEST_TRANSFORMATION_NAME,
            }, data={
                'arguments': TEST_TRANSFORMATION_ARGUMENT
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
                'arguments': TEST_TRANSFORMATION_ARGUMENT_EDITED
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
                'transformation': TEST_TRANSFORMATION_CLASS_NAME
            }
        )
