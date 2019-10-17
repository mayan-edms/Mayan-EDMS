from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.converter.models import ObjectLayer
from mayan.apps.converter.tests.mixins import LayerTestMixin
from mayan.apps.permissions.tests.mixins import PermissionTestMixin

from ..layers import layer_redactions

from .literals import (
    TEST_REDACTION_NAME, TEST_REDACTION_ARGUMENT,
    TEST_REDACTION_ARGUMENT_EDITED
)

'''
class RedactionLayerTestMixin(PermissionTestMixin):
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
'''


class RedactionTestMixin(object):
    def setUp(self):
        super(RedactionTestMixin, self).setUp()
        self.test_layer = layer_redactions

    def _create_test_redaction(self):
        content_type = ContentType.objects.get_for_model(model=self.test_document)
        object_layer, created = ObjectLayer.objects.get_or_create(
            content_type=content_type, object_id=self.test_document.pk,
            stored_layer=self.test_layer.stored_layer
        )

        self.test_redaction = object_layer.transformations.create(
            name=TEST_REDACTION_NAME,
            arguments=TEST_REDACTION_ARGUMENT
        )


class RedactionViewsTestMixin(object):
    def _request_redaction_create_view(self):
        return self.post(
            viewname='converter:transformation_create', kwargs={
                'app_label': 'documents', 'model': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name,
                'redaction_name': TEST_REDACTION_NAME,
            }, data={
                'arguments': TEST_REDACTION_ARGUMENT
            }
        )

    def _request_redaction_delete_view(self):
        return self.post(
            viewname='converter:transformation_delete', kwargs={
                'layer_name': self.test_layer.name,
                'pk': self.test_redaction.pk
            }
        )

    def _request_redaction_edit_view(self):
        return self.post(
            viewname='converter:transformation_edit', kwargs={
                'layer_name': self.test_layer.name,
                'pk': self.test_redaction.pk
            }, data={
                'arguments': TEST_REDACTION_ARGUMENT_EDITED
            }
        )

    def _request_redaction_list_view(self):
        return self.get(
            viewname='converter:transformation_list', kwargs={
                'app_label': 'documents', 'model': 'document',
                'object_id': self.test_document.pk,
                'layer_name': self.test_layer.name
            }
        )
