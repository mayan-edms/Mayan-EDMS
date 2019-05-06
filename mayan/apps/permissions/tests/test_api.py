from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.rest_api.tests import BaseAPITestCase
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from ..classes import Permission
from ..models import Role
from ..permissions import (
    permission_role_create, permission_role_delete,
    permission_role_edit, permission_role_view
)

from .mixins import (
    PermissionAPIViewTestMixin, PermissionTestMixin, RoleAPIViewTestMixin,
    RoleTestMixin
)


class PermissionAPIViewTestCase(PermissionAPIViewTestMixin, BaseAPITestCase):
    def setUp(self):
        super(PermissionAPIViewTestCase, self).setUp()
        Permission.invalidate_cache()

    def test_permissions_list_api_view(self):
        response = self._request_permissions_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoleAPIViewTestCase(GroupTestMixin, PermissionTestMixin, RoleAPIViewTestMixin, RoleTestMixin, BaseAPITestCase):
    def test_role_create_api_view_no_permission(self):
        role_count = Role.objects.count()

        response = self._request_test_role_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Role.objects.count(), role_count)

    def test_role_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_role_create)

        role_count = Role.objects.count()

        response = self._request_test_role_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Role.objects.count(), role_count + 1)

    def _request_role_create_api_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self.test_group.pk),
            'permissions_pk_list': '{}'.format(self.test_permission.pk)
        }
        return self._request_test_role_create_api_view(extra_data=extra_data)

    def test_role_create_api_view_extra_data_no_permission(self):
        self._create_test_group()
        self._create_test_permission()

        role_count = Role.objects.count()

        response = self._request_role_create_api_view_extra_data()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Role.objects.count(), role_count)

    def test_role_create_complex_view_with_permission(self):
        self._create_test_group()
        self._create_test_permission()

        self.grant_permission(permission=permission_role_create)

        role_count = Role.objects.count()

        response = self._request_role_create_api_view_extra_data()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Role.objects.count(), role_count + 1)

        new_role = Role.objects.get(pk=response.data['id'])

        self.assertTrue(
            self.test_group in new_role.groups.all()
        )
        self.assertTrue(
            self.test_permission.stored_permission in new_role.permissions.all()
        )

    def test_role_delete_view_no_access(self):
        self._create_test_role()

        role_count = Role.objects.count()

        response = self._request_test_role_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Role.objects.count(), role_count)

    def test_role_delete_view_with_access(self):
        self._create_test_role()

        self.grant_access(obj=self.test_role, permission=permission_role_delete)

        role_count = Role.objects.count()

        response = self._request_test_role_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Role.objects.count(), role_count - 1)

    def test_role_edit_via_patch_no_access(self):
        self._create_test_role()

        response = self._request_test_role_edit_api_view(request_type='patch')

        role_label = self.test_role.label

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_role.refresh_from_db()
        self.assertEqual(self.test_role.label, role_label)

    def test_role_edit_via_patch_with_access(self):
        self._create_test_role()
        self.grant_access(obj=self.test_role, permission=permission_role_edit)

        role_label = self.test_role.label

        response = self._request_test_role_edit_api_view(request_type='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_role.refresh_from_db()
        self.assertNotEqual(self.test_role.label, role_label)

    def test_role_edit_via_put_no_access(self):
        self._create_test_role()

        response = self._request_test_role_edit_api_view(request_type='put')

        role_label = self.test_role.label

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_role.refresh_from_db()
        self.assertEqual(self.test_role.label, role_label)

    def test_role_edit_via_put_with_access(self):
        self._create_test_role()
        self.grant_access(obj=self.test_role, permission=permission_role_edit)

        role_label = self.test_role.label

        response = self._request_test_role_edit_api_view(request_type='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_role.refresh_from_db()
        self.assertNotEqual(self.test_role.label, role_label)

    def _request_role_edit_api_patch_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self.test_group.pk),
            'permissions_pk_list': '{}'.format(self.test_permission.pk)
        }
        return self._request_test_role_edit_api_view(
            extra_data=extra_data, request_type='patch'
        )

    def test_role_edit_api_patch_view_extra_data_no_access(self):
        self._create_test_group()
        self._create_test_permission()
        self._create_test_role()

        role_label = self.test_role.label

        response = self._request_role_edit_api_patch_view_extra_data()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_role.refresh_from_db()
        self.assertEqual(self.test_role.label, role_label)
        self.assertTrue(
            self.test_group not in self.test_role.groups.all()
        )
        self.assertTrue(
            self.test_permission.stored_permission not in self.test_role.permissions.all()
        )

    def test_role_edit_api_patch_view_extra_data_with_access(self):
        self._create_test_group()
        self._create_test_permission()
        self._create_test_role()

        self.grant_access(obj=self.test_role, permission=permission_role_edit)

        role_label = self.test_role.label

        response = self._request_role_edit_api_patch_view_extra_data()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_role.refresh_from_db()
        self.assertNotEqual(self.test_role.label, role_label)
        self.assertTrue(
            self.test_group in self.test_role.groups.all()
        )
        self.assertTrue(
            self.test_permission.stored_permission in self.test_role.permissions.all()
        )

    def _request_role_edit_api_put_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self.test_group.pk),
            'permissions_pk_list': '{}'.format(self.test_permission.pk)
        }
        return self._request_test_role_edit_api_view(
            extra_data=extra_data, request_type='put'
        )

    def test_role_edit_api_put_view_extra_data_no_access(self):
        self._create_test_group()
        self._create_test_permission()
        self._create_test_role()

        role_label = self.test_role.label

        response = self._request_role_edit_api_put_view_extra_data()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_role.refresh_from_db()
        self.assertEqual(self.test_role.label, role_label)
        self.assertTrue(
            self.test_group not in self.test_role.groups.all()
        )
        self.assertTrue(
            self.test_permission.stored_permission not in self.test_role.permissions.all()
        )

    def test_role_edit_api_put_view_extra_data_with_access(self):
        self._create_test_group()
        self._create_test_permission()
        self._create_test_role()

        self.grant_access(obj=self.test_role, permission=permission_role_edit)

        role_label = self.test_role.label

        response = self._request_role_edit_api_put_view_extra_data()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_role.refresh_from_db()
        self.assertNotEqual(self.test_role.label, role_label)
        self.assertTrue(
            self.test_group in self.test_role.groups.all()
        )
        self.assertTrue(
            self.test_permission.stored_permission in self.test_role.permissions.all()
        )

    def test_roles_list_view_no_access(self):
        self._create_test_role()

        response = self._request_role_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

    def test_roles_list_view_with_access(self):
        self._create_test_role()
        self.grant_access(
            obj=self.test_role, permission=permission_role_view
        )

        response = self._request_role_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_role.label
        )
