from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from .mixins import RoleTestMixin


class RoleCopyTestCase(
    GroupTestMixin, ObjectCopyTestMixin, RoleTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_permission()
        self._create_test_role()
        self._create_test_group()
        self._test_role.grant(permission=self._test_permission)
        self._test_role.groups.add(self._test_group)
        self._test_object = self._test_role
