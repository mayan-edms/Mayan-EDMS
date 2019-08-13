from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import status

from mayan.apps.rest_api.tests import BaseAPITestCase

from ..permissions import (
    permission_group_create, permission_group_delete,
    permission_group_edit, permission_group_view,
    permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)

from .mixins import GroupAPITestMixin, GroupTestMixin, UserAPITestMixin


class GroupAPITestCase(GroupAPITestMixin, GroupTestMixin, BaseAPITestCase):
    def test_group_create_no_permission(self):
        group_count = Group.objects.count()

        response = self._request_test_group_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Group.objects.count(), group_count)

    def test_group_create_with_permission(self):
        self.grant_permission(permission=permission_group_create)

        group_count = Group.objects.count()

        response = self._request_test_group_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Group.objects.count(), group_count + 1)

    def test_group_delete_no_access(self):
        self._create_test_group()
        group_count = Group.objects.count()

        response = self._request_test_group_delete_api_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Group.objects.count(), group_count)

    def test_group_delete_with_access(self):
        self._create_test_group()
        self.grant_access(obj=self.test_group, permission=permission_group_delete)
        group_count = Group.objects.count()

        response = self._request_test_group_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Group.objects.count(), group_count - 1)

    def test_group_edit_via_patch_no_access(self):
        self._create_test_group()

        group_name = self.test_group.name

        response = self._request_test_group_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, group_name)

    def test_group_edit_via_patch_with_access(self):
        self._create_test_group()

        self.grant_access(obj=self.test_group, permission=permission_group_edit)

        group_name = self.test_group.name

        response = self._request_test_group_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_group.refresh_from_db()
        self.assertNotEqual(self.test_group.name, group_name)

    def test_group_edit_via_put_no_access(self):
        self._create_test_group()

        group_name = self.test_group.name

        response = self._request_test_group_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, group_name)

    def test_group_edit_via_put_with_access(self):
        self._create_test_group()

        self.grant_access(obj=self.test_group, permission=permission_group_edit)

        group_name = self.test_group.name

        response = self._request_test_group_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_group.refresh_from_db()
        self.assertNotEqual(self.test_group.name, group_name)


class UserAPITestCase(UserAPITestMixin, BaseAPITestCase):
    def test_user_create_api_view_no_permission(self):
        user_count = get_user_model().objects.count()

        response = self._request_test_user_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(get_user_model().objects.count(), user_count)

    def test_user_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_user_create)

        user_count = get_user_model().objects.count()

        response = self._request_test_user_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(get_user_model().objects.count(), user_count + 1)

    def test_user_delete_no_access(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        response = self._request_test_user_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(get_user_model().objects.count(), user_count)

    def test_user_delete_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_delete)

        user_count = get_user_model().objects.count()

        response = self._request_test_user_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(get_user_model().objects.count(), user_count - 1)

    def test_user_edit_patch_api_view_no_access(self):
        self._create_test_user()

        user_username = self.test_user.username

        response = self._request_test_user_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, user_username)

    def test_user_edit_patch_api_view_with_access(self):
        self._create_test_user()

        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        user_username = self.test_user.username
        response = self._request_test_user_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.username, user_username)

    def test_user_edit_put_api_view_no_access(self):
        self._create_test_user()

        user_username = self.test_user.username

        response = self._request_test_user_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, user_username)

    def test_user_edit_put_api_view_with_access(self):
        self._create_test_user()

        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        user_username = self.test_user.username
        response = self._request_test_user_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.username, user_username)


class UserGroupAPITestCase(GroupTestMixin, UserAPITestMixin, BaseAPITestCase):
    def test_user_create_with_group_api_view_no_permission(self):
        self._create_test_group()

        user_count = get_user_model().objects.count()

        response = self._request_test_user_create_api_view_extra_data()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(get_user_model().objects.count(), user_count)

    def test_user_create_with_group_api_view_with_permission(self):
        self._create_test_group()
        self.grant_permission(permission=permission_user_create)

        user_count = get_user_model().objects.count()

        response = self._request_test_user_create_api_view_extra_data()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(get_user_model().objects.count(), user_count + 1)

        self.test_user.refresh_from_db()
        self.assertTrue(self.test_group in self.test_user.groups.all())

    def test_user_group_add_api_view_no_permission(self):
        self._create_test_user()
        self._create_test_group()

        user_group_count = self.test_user.groups.count()

        response = self._request_test_user_group_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.groups.count(), user_group_count)

    def test_user_group_add_api_view_with_user_access(self):
        self._create_test_user()
        self._create_test_group()

        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        user_group_count = self.test_user.groups.count()

        response = self._request_test_user_group_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_user.refresh_from_db()

        self.assertEqual(self.test_user.groups.count(), user_group_count)

    def test_user_group_add_api_view_with_group_access(self):
        self._create_test_user()
        self._create_test_group()

        self.grant_access(obj=self.test_group, permission=permission_group_view)

        user_group_count = self.test_user.groups.count()

        response = self._request_test_user_group_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.groups.count(), user_group_count)

    def test_user_group_add_api_view_with_full_access(self):
        self._create_test_user()
        self._create_test_group()

        self.grant_access(obj=self.test_user, permission=permission_user_edit)
        self.grant_access(obj=self.test_group, permission=permission_group_view)

        user_group_count = self.test_user.groups.count()

        response = self._request_test_user_group_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.groups.count(), user_group_count + 1)

    def _create_test_user_with_test_group(self):
        self._create_test_group()
        self._create_test_user()
        self.test_user.groups.add(self.test_group)

    def test_user_group_list_no_access(self):
        self._create_test_user_with_test_group()

        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_group_list_with_user_access(self):
        self._create_test_user_with_test_group()

        self.grant_access(obj=self.test_user, permission=permission_user_view)
        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_user_group_list_with_group_access(self):
        self._create_test_user_with_test_group()

        self.grant_access(obj=self.test_group, permission=permission_group_view)
        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_group_list_with_full_access(self):
        self._create_test_user_with_test_group()

        self.grant_access(obj=self.test_user, permission=permission_user_view)
        self.grant_access(obj=self.test_group, permission=permission_group_view)
        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_user_login_api_view(self):
        self._create_test_user()

        self.assertTrue(
            self.login(
                username=self.test_user.username,
                password=self.test_user.cleartext_password
            )
        )

    def test_user_create_login_password_change_api_view_no_access(self):
        self._create_test_user()

        response = self._request_test_user_password_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(
            self.login(
                username=self.test_user.username,
                password=self.test_user.cleartext_password
            )
        )

    def test_user_create_login_password_change_api_view_with_access(self):
        self._create_test_user()

        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        response = self._request_test_user_password_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            self.login(
                username=self.test_user.username,
                password=self.test_user.cleartext_password
            )
        )
