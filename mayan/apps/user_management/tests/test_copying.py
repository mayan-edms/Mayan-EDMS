from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import GroupTestMixin


class GroupCopyTestCase(
    GroupTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()
        self.test_user.groups.add(self.test_group)
        self.test_object = self.test_group


class UserCopyTestCase(
    GroupTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()
        self.test_user.groups.add(self.test_group)
        self.test_object = self.test_user
