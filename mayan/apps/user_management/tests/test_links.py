from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import (
    permission_group_create, permission_group_view, permission_user_create,
    permission_user_view
)

from .mixins import GroupLinkTestMixin, GroupTestMixin, UserLinkTestMixin


class GroupLinkTestCase(
    GroupLinkTestMixin, GroupTestMixin, GenericViewTestCase
):
    def test_group_setup_link_no_permission(self):
        resolved_link = self._resolve_group_setup_link()
        self.assertEqual(resolved_link, None)

    def test_group_setup_link_with_create_permission(self):
        self.grant_permission(permission=permission_group_create)
        resolved_link = self._resolve_group_setup_link()
        self.assertNotEqual(resolved_link, None)

    def test_group_setup_link_with_view_access(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )
        resolved_link = self._resolve_group_setup_link()
        self.assertNotEqual(resolved_link, None)


class UserLinkTestCase(UserLinkTestMixin, GenericViewTestCase):
    def test_user_setup_link_no_permission(self):
        resolved_link = self._resolve_user_setup_link()
        self.assertEqual(resolved_link, None)

    def test_user_setup_link_with_create_permission(self):
        self.grant_permission(permission=permission_user_create)
        resolved_link = self._resolve_user_setup_link()
        self.assertNotEqual(resolved_link, None)

    def test_user_setup_link_with_view_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_view
        )
        resolved_link = self._resolve_user_setup_link()
        self.assertNotEqual(resolved_link, None)
