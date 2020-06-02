from mayan.apps.tests.tests.base import GenericViewTestCase
from mayan.apps.user_management.permissions import permission_group_edit
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from ..models import Role
from ..permissions import (
    permission_role_create, permission_role_delete, permission_role_edit,
    permission_role_view
)

from .mixins import GroupRoleViewTestMixin, RoleTestMixin, RoleViewTestMixin


class RolePermissionViewsTestCase(
    RoleTestMixin, RoleViewTestMixin, GenericViewTestCase
):
    def test_role_permissions_view_with_access(self):
        """
        Tests that a defined permission is available before it is ever used
        or referenced. Tests the runtime permission to stored permission
        cache initialization.
        https://forum.mayan-edms.com/viewtopic.php?f=7&t=1614
        GitLab issue #757 "Permissions list does not show an object until
        one has been created"
        """
        self._create_test_role()

        self.grant_access(
            obj=self.test_role, permission=permission_role_edit
        )

        response = self._request_test_role_permissions_view()
        self.assertContains(
            response=response, status_code=200,
            text=permission_role_view.label
        )


class RoleViewsTestCase(
    RoleTestMixin, RoleViewTestMixin, GenericViewTestCase
):
    def test_role_creation_view_no_permission(self):
        role_count = Role.objects.count()

        response = self._request_test_role_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Role.objects.count(), role_count)

    def test_role_creation_view_with_permission(self):
        self.grant_permission(permission=permission_role_create)
        role_count = Role.objects.count()

        response = self._request_test_role_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Role.objects.count(), role_count + 1)

    def test_role_delete_view_no_permission(self):
        self._create_test_role()

        role_count = Role.objects.count()

        response = self._request_test_role_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Role.objects.count(), role_count)

    def test_role_delete_view_with_access(self):
        self._create_test_role()
        self.grant_access(
            obj=self.test_role, permission=permission_role_delete
        )

        role_count = Role.objects.count()

        response = self._request_test_role_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Role.objects.count(), role_count - 1)

    def test_role_edit_view_no_permission(self):
        self._create_test_role()
        role_label = self.test_role.label

        response = self._request_test_role_edit_view()

        self.assertEqual(response.status_code, 404)

        self.test_role.refresh_from_db()
        self.assertEqual(self.test_role.label, role_label)

    def test_role_edit_view_with_access(self):
        self._create_test_role()
        self.grant_access(obj=self.test_role, permission=permission_role_edit)

        role_label = self.test_role.label

        response = self._request_test_role_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_role.refresh_from_db()
        self.assertNotEqual(self.test_role.label, role_label)

    def test_role_list_view_no_permission(self):
        self._create_test_role()

        response = self._request_test_role_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, text=self.test_role.label, status_code=200
        )

    def test_role_list_view_with_access(self):
        self._create_test_role()
        self.grant_access(obj=self.test_role, permission=permission_role_view)

        response = self._request_test_role_list_view()
        self.assertContains(
            response=response, text=self.test_role.label, status_code=200
        )

    def test_role_permissions_view_no_permission(self):
        self._create_test_role()

        response = self._request_test_role_permissions_view()
        self.assertEqual(response.status_code, 404)

    def test_role_permissions_view_with_access(self):
        self._create_test_role()
        self.grant_access(
            obj=self.test_role, permission=permission_role_edit
        )

        response = self._request_test_role_permissions_view()
        self.assertEqual(response.status_code, 200)

    def test_role_groups_view_no_permission(self):
        self._create_test_role()

        response = self._request_test_role_groups_view()
        self.assertEqual(response.status_code, 404)

    def test_role_groups_view_with_access(self):
        self._create_test_role()
        self.grant_access(
            obj=self.test_role, permission=permission_role_edit
        )

        response = self._request_test_role_groups_view()
        self.assertEqual(response.status_code, 200)


class GroupRoleViewTestCase(
    GroupTestMixin, GroupRoleViewTestMixin, RoleTestMixin, GenericViewTestCase
):
    def test_group_roles_view_no_permission(self):
        self._create_test_group()

        response = self._request_test_group_roles_view()
        self.assertEqual(response.status_code, 404)

    def test_group_roles_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        response = self._request_test_group_roles_view()
        self.assertEqual(response.status_code, 200)
