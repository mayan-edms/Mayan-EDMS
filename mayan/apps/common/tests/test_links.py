from django.db import models

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import ModelCopy
from ..permissions import permission_object_copy

from .literals import TEST_OBJECT_LABEL
from .mixins import ObjectCopyLinkTestMixin


class ObjectCopyLinkTestCase(
    ObjectCopyLinkTestMixin, GenericViewTestCase
):
    auto_create_test_object = True
    auto_create_test_object_fields = {
        'label': models.CharField(max_length=32, unique=True)
    }
    auto_create_test_object_instance_kwargs = {
        'label': TEST_OBJECT_LABEL
    }

    def setUp(self):
        super().setUp()
        ModelCopy(model=self.TestModel, register_permission=True).add_fields(
            field_names=('label',)
        )

    def test_object_copy_link_no_permission(self):
        resolved_link = self._resolve_test_object_copy_link()
        self.assertEqual(resolved_link, None)

    def test_object_copy_link_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_object_copy
        )
        resolved_link = self._resolve_test_object_copy_link()
        self.assertNotEqual(resolved_link, None)
