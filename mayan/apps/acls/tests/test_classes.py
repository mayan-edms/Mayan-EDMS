from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests.base import BaseTestCase

from ..classes import ModelPermission


class ModelPermissionTestCase(BaseTestCase):
    def test_model_permission_get_classes_as_content_type(self):
        self.assertNotEqual(
            ModelPermission.get_classes(as_content_type=True).count(), 0
        )
