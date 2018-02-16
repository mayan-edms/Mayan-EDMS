from __future__ import unicode_literals

from django.contrib.auth.models import Group

from rest_framework import status

from rest_api.tests import BaseAPITestCase
from user_management.tests.literals import TEST_GROUP_2_NAME

from ..classes import Permission
from ..models import Role
from ..permissions import (
    permission_role_create, permission_role_delete,
    permission_role_edit, permission_role_view
)

from .literals import (
    TEST_ROLE_2_LABEL, TEST_ROLE_LABEL, TEST_ROLE_LABEL_EDITED
)


class PermissionAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(PermissionAPITestCase, self).setUp()
        self.login_user()
        Permission.invalidate_cache()

    def test_permissions_list_view(self):
        response = self.get(viewname='rest_api:permission-list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Role view

    def test_roles_list_view_no_access(self):
        response = self.get(viewname='rest_api:role-list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_roles_list_view_with_access(self):
        self.grant_access(
            permission=permission_role_view, obj=self.role
        )
        response = self.get(viewname='rest_api:role-list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['label'], self.role.label)

    # Role create

    def _role_create_request(self, extra_data=None):
        data = {
            'label': TEST_ROLE_2_LABEL
        }

        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='rest_api:role-list', data=data
        )

    def test_role_create_view_no_permission(self):
        response = self._role_create_request()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Role.objects.count(), 1)

    def test_role_create_view_with_permission(self):
        self.grant_permission(permission=permission_role_create)
        response = self._role_create_request()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        role = Role.objects.get(label=TEST_ROLE_2_LABEL)
        self.assertEqual(response.data, {'label': role.label, 'id': role.pk})
        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(role.label, TEST_ROLE_2_LABEL)

    def _create_group(self):
        self.group_2 = Group.objects.create(name=TEST_GROUP_2_NAME)

    def _request_role_create_with_extra_data(self):
        self._create_group()

        return self._role_create_request(
            extra_data={
                'groups_pk_list': '{}'.format(self.group_2.pk),
                'permissions_pk_list': '{}'.format(permission_role_view.pk)
            }
        )

    def test_role_create_complex_view_no_permission(self):
        response = self._request_role_create_with_extra_data()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(
            list(Role.objects.values_list('label', flat=True)),
            [TEST_ROLE_LABEL]
        )

    def test_role_create_complex_view_with_permission(self):
        self.grant_permission(permission=permission_role_create)
        response = self._request_role_create_with_extra_data()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)
        role = Role.objects.get(label=TEST_ROLE_2_LABEL)
        self.assertEqual(role.label, TEST_ROLE_2_LABEL)
        self.assertQuerysetEqual(
            role.groups.all(), (repr(self.group_2),)
        )
        self.assertQuerysetEqual(
            role.permissions.all(),
            (repr(permission_role_view.stored_permission),)
        )

    # Role edit

    def _request_role_edit(self, extra_data=None, request_type='patch'):
        data = {
            'label': TEST_ROLE_LABEL_EDITED
        }

        if extra_data:
            data.update(extra_data)

        return getattr(self, request_type)(
            viewname='rest_api:role-detail', args=(self.role.pk,),
            data=data
        )

    def test_role_edit_via_patch_no_access(self):
        response = self._request_role_edit(request_type='patch')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL)

    def test_role_edit_via_patch_with_access(self):
        self.grant_access(permission=permission_role_edit, obj=self.role)
        response = self._request_role_edit(request_type='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL_EDITED)

    def _request_role_edit_via_patch_with_extra_data(self):
        self._create_group()
        return self._request_role_edit(
            extra_data={
                'groups_pk_list': '{}'.format(self.group_2.pk),
                'permissions_pk_list': '{}'.format(permission_role_view.pk)
            },
            request_type='patch'
        )

    def test_role_edit_complex_via_patch_no_access(self):
        response = self._request_role_edit_via_patch_with_extra_data()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL)

        self.assertQuerysetEqual(
            self.role.groups.all(), (repr(self.group),)
        )
        self.assertQuerysetEqual(self.role.permissions.all(), ())

    def test_role_edit_complex_via_patch_with_access(self):
        self.grant_access(permission=permission_role_edit, obj=self.role)
        response = self._request_role_edit_via_patch_with_extra_data()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL_EDITED)
        self.assertQuerysetEqual(
            self.role.groups.all(), (repr(self.group_2),)
        )
        self.assertQuerysetEqual(
            self.role.permissions.all(),
            (repr(permission_role_view.stored_permission),)
        )

    def test_role_edit_via_put_no_access(self):
        response = self._request_role_edit(request_type='put')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL)

    def test_role_edit_via_put_with_access(self):
        self.grant_access(permission=permission_role_edit, obj=self.role)
        response = self._request_role_edit(request_type='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL_EDITED)

    def _request_role_edit_via_put_with_extra_data(self):
        self._create_group()

        return self._request_role_edit(
            extra_data={
                'groups_pk_list': '{}'.format(self.group_2.pk),
                'permissions_pk_list': '{}'.format(permission_role_view.pk)
            }, request_type='put'
        )

    def test_role_edit_complex_via_put_no_access(self):
        response = self._request_role_edit_via_put_with_extra_data()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL)
        self.assertQuerysetEqual(
            self.role.groups.all(), (repr(self.group),)
        )
        self.assertQuerysetEqual(
            self.role.permissions.all(),
            ()
        )

    def test_role_edit_complex_via_put_with_access(self):
        self.grant_access(permission=permission_role_edit, obj=self.role)
        response = self._request_role_edit_via_put_with_extra_data()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.label, TEST_ROLE_LABEL_EDITED)
        self.assertQuerysetEqual(
            self.role.groups.all(), (repr(self.group_2),)
        )
        self.assertQuerysetEqual(
            self.role.permissions.all(),
            (repr(permission_role_view.stored_permission),)
        )

    # Role delete

    def _request_role_delete_view(self):
        return self.delete(
            viewname='rest_api:role-detail', args=(self.role.pk,)
        )

    def test_role_delete_view_no_access(self):
        response = self._request_role_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Role.objects.count(), 1)

    def test_role_delete_view_with_access(self):
        self.grant_access(permission=permission_role_delete, obj=self.role)
        response = self._request_role_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Role.objects.count(), 0)
