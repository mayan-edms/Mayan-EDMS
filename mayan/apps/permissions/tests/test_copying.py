from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.tests.tests.base import BaseTestCase
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from .mixins import PermissionTestMixin, RoleTestMixin


class RoleCopyTestCase(
    GroupTestMixin, ObjectCopyTestMixin, PermissionTestMixin, RoleTestMixin,
    BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_permission()
        self._create_test_role()
        self._create_test_group()
        self.test_role.grant(permission=self.test_permission)
        self.test_role.groups.add(self.test_group)
        self.test_object = self.test_role
