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
        self._test_user.groups.add(self._test_group)
        self._test_object = self._test_group


class UserCopyTestCase(
    GroupTestMixin, ObjectCopyTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()
        self._test_user.groups.add(self._test_group)
        self._test_object = self._test_user
