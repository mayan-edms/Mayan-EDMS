from __future__ import unicode_literals

from django.contrib.auth.models import Group

from common.tests import GenericViewTestCase
from user_management.permissions import permission_group_edit
from user_management.tests.literals import TEST_GROUP_2_NAME

from ..models import Role
from ..permissions import (
    permission_permission_grant, permission_permission_revoke,
    permission_role_create, permission_role_delete, permission_role_edit,
    permission_role_view,
)

from .literals import TEST_ROLE_2_LABEL, TEST_ROLE_LABEL_EDITED


class PermissionsViewsTestCase(GenericViewTestCase):
    def setUp(self):
        super(PermissionsViewsTestCase, self).setUp()
        self.login_user()

    def _request_create_role_view(self):
        return self.post(
            viewname='permissions:role_create', data={
                'label': TEST_ROLE_2_LABEL,
            }
        )

    def test_role_creation_view_no_permission(self):
        response = self._request_create_role_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Role.objects.count(), 1)
        self.assertFalse(TEST_ROLE_2_LABEL in Role.objects.values_list('label', flat=True))

    def test_role_creation_view_with_permission(self):
        self.grant_permission(permission=permission_role_create)
        response = self._request_create_role_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Role.objects.count(), 2)
        self.assertTrue(TEST_ROLE_2_LABEL in Role.objects.values_list('label', flat=True))

    def _request_role_delete_view(self):
        return self.post(
            viewname='permissions:role_delete', args=(self.role_2.pk,),
        )

    def _create_role(self):
        self.role_2 = Role.objects.create(label=TEST_ROLE_2_LABEL)

    def test_role_delete_view_no_access(self):
        self._create_role()
        response = self._request_role_delete_view()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Role.objects.count(), 2)
        self.assertTrue(TEST_ROLE_2_LABEL in Role.objects.values_list('label', flat=True))

    def test_role_delete_view_with_access(self):
        self._create_role()
        self.grant_access(permission=permission_role_delete, obj=self.role_2)
        response = self._request_role_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Role.objects.count(), 1)
        self.assertFalse(TEST_ROLE_2_LABEL in Role.objects.values_list('label', flat=True))

    def _request_role_edit_view(self):
        return self.post(
            viewname='permissions:role_edit', args=(self.role_2.pk,), data={
                'label': TEST_ROLE_LABEL_EDITED,
            }
        )

    def test_role_edit_view_no_access(self):
        self._create_role()
        response = self._request_role_edit_view()

        self.assertEqual(response.status_code, 403)

        self.role_2.refresh_from_db()
        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(self.role_2.label, TEST_ROLE_2_LABEL)

    def test_role_edit_view_with_access(self):
        self._create_role()
        self.grant_access(permission=permission_role_edit, obj=self.role_2)
        response = self._request_role_edit_view()

        self.assertEqual(response.status_code, 302)
        self.role_2.refresh_from_db()

        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(self.role_2.label, TEST_ROLE_LABEL_EDITED)

    def _request_role_list_view(self):
        return self.get(viewname='permissions:role_list')

    def test_role_list_view_no_access(self):
        self._create_role()
        response = self._request_role_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, text=TEST_ROLE_2_LABEL, status_code=200)

    def test_role_list_view_with_access(self):
        self._create_role()
        self.grant_access(permission=permission_role_view, obj=self.role_2)
        response = self._request_role_list_view()
        self.assertContains(response, text=TEST_ROLE_2_LABEL, status_code=200)

    def _request_role_permissions_view(self):
        return self.get(
            viewname='permissions:role_permissions', args=(self.role_2.pk,)
        )

    def test_role_permissions_view_no_access(self):
        self._create_role()
        response = self._request_role_permissions_view()
        self.assertEqual(response.status_code, 403)

    def test_role_permissions_view_with_permission_grant(self):
        self._create_role()
        self.grant_access(permission=permission_permission_grant, obj=self.role_2)
        response = self._request_role_permissions_view()
        self.assertEqual(response.status_code, 200)

    def test_role_permissions_view_with_permission_revoke(self):
        self._create_role()
        self.grant_access(permission=permission_permission_revoke, obj=self.role_2)
        response = self._request_role_permissions_view()
        self.assertEqual(response.status_code, 200)

    def _request_role_groups_view(self):
        return self.get(
            viewname='permissions:role_groups', args=(self.role_2.pk,)
        )

    def test_role_groups_view_no_access(self):
        self._create_role()
        response = self._request_role_groups_view()
        self.assertEqual(response.status_code, 403)

    def test_role_groups_view_with_access(self):
        self._create_role()
        self.grant_access(permission=permission_role_edit, obj=self.role_2)
        response = self._request_role_groups_view()
        self.assertEqual(response.status_code, 200)

    def _create_group(self):
        self.group_2 = Group.objects.create(name=TEST_GROUP_2_NAME)

    def _request_group_roles_view(self):
        return self.get(
            viewname='permissions:group_roles', args=(self.group_2.pk,)
        )

    def test_group_roles_view_no_access(self):
        self._create_group()
        response = self._request_group_roles_view()
        self.assertEqual(response.status_code, 403)

    def test_group_roles_view_with_access(self):
        self._create_group()
        self.grant_access(permission=permission_group_edit, obj=self.group_2)
        response = self._request_group_roles_view()
        self.assertEqual(response.status_code, 200)
