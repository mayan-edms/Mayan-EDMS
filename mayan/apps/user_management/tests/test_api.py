from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import status

from rest_api.tests import BaseAPITestCase

from ..permissions import (
    permission_group_create, permission_group_delete,
    permission_group_edit, permission_group_view,
    permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)

from .literals import (
    TEST_GROUP_2_NAME, TEST_GROUP_2_NAME_EDITED, TEST_USER_2_EMAIL,
    TEST_USER_2_PASSWORD, TEST_USER_2_USERNAME, TEST_USER_2_USERNAME_EDITED,
    TEST_USER_2_PASSWORD_EDITED
)


class UserManagementUserAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(UserManagementUserAPITestCase, self).setUp()
        self.login_user()

    # User create

    def _create_user(self):
        return get_user_model().objects.create_user(
            username=TEST_USER_2_USERNAME, email=TEST_USER_2_EMAIL,
            password=TEST_USER_2_PASSWORD
        )

    def _request_user_create(self):
        return self.post(
            viewname='rest_api:user-list', data={
                'email': TEST_USER_2_EMAIL, 'password': TEST_USER_2_PASSWORD,
                'username': TEST_USER_2_USERNAME,
            }
        )

    def test_user_create_no_permission(self):
        response = self._request_user_create()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Default two users, the test admin and the test user
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_user_create_with_permission(self):
        self.grant_permission(permission=permission_user_create)
        response = self._request_user_create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=response.data['id'])
        self.assertEqual(user.username, TEST_USER_2_USERNAME)
        self.assertEqual(get_user_model().objects.count(), 3)

    def _request_create_user_with_extra_data(self):
        return self.post(
            viewname='rest_api:user-list', data={
                'email': TEST_USER_2_EMAIL, 'password': TEST_USER_2_PASSWORD,
                'username': TEST_USER_2_USERNAME,
                'groups_pk_list': self.groups_pk_list
            }
        )

    def test_user_create_with_group_no_permission(self):
        group_1 = Group.objects.create(name=TEST_GROUP_2_NAME)
        self.groups_pk_list = '{}'.format(group_1.pk)

        response = self._request_create_user_with_extra_data()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_with_group_with_permission(self):
        group_1 = Group.objects.create(name=TEST_GROUP_2_NAME)
        self.groups_pk_list = '{}'.format(group_1.pk)

        self.grant_permission(permission=permission_user_create)
        response = self._request_create_user_with_extra_data()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(pk=response.data['id'])
        self.assertEqual(user.username, TEST_USER_2_USERNAME)
        self.assertQuerysetEqual(user.groups.all(), (repr(group_1),))

    def test_user_create_with_groups_no_permission(self):
        group_1 = Group.objects.create(name='test group 1')
        group_2 = Group.objects.create(name='test group 2')
        self.groups_pk_list = '{},{}'.format(group_1.pk, group_2.pk)
        response = self._request_create_user_with_extra_data()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_with_groups_with_permission(self):
        group_1 = Group.objects.create(name='test group 1')
        group_2 = Group.objects.create(name='test group 2')
        self.groups_pk_list = '{},{}'.format(group_1.pk, group_2.pk)
        self.grant_permission(permission=permission_user_create)
        response = self._request_create_user_with_extra_data()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(pk=response.data['id'])
        self.assertEqual(user.username, TEST_USER_2_USERNAME)
        self.assertQuerysetEqual(
            user.groups.all().order_by('name'), (repr(group_1), repr(group_2))
        )

    # User login

    def test_user_create_login(self):
        self._create_user()

        self.assertTrue(
            self.login(
                username=TEST_USER_2_USERNAME, password=TEST_USER_2_PASSWORD
            )
        )

    # User password change

    def test_user_create_login_password_change_no_access(self):
        user = self._create_user()

        self.patch(
            viewname='rest_api:user-detail', args=(user.pk,), data={
                'password': TEST_USER_2_PASSWORD_EDITED,
            }
        )

        self.assertFalse(
            self.client.login(
                username=TEST_USER_2_USERNAME, password=TEST_USER_2_PASSWORD_EDITED
            )
        )

    def test_user_create_login_password_change_with_access(self):
        user = self._create_user()

        self.grant_access(permission=permission_user_edit, obj=user)
        self.patch(
            viewname='rest_api:user-detail', args=(user.pk,), data={
                'password': TEST_USER_2_PASSWORD_EDITED,
            }
        )

        self.assertTrue(
            self.client.login(
                username=TEST_USER_2_USERNAME, password=TEST_USER_2_PASSWORD_EDITED
            )
        )

    # User edit

    def _request_user_edit_via_put(self, user):
        return self.put(
            viewname='rest_api:user-detail', args=(user.pk,),
            data={'username': TEST_USER_2_USERNAME_EDITED}
        )

    def test_user_edit_via_put_no_access(self):
        user = self._create_user()
        response = self._request_user_edit_via_put(user=user)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_2_USERNAME)

    def test_user_edit_via_put_with_access(self):
        user = self._create_user()
        self.grant_access(permission=permission_user_edit, obj=user)
        response = self._request_user_edit_via_put(user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_2_USERNAME_EDITED)

    def _request_user_edit_via_patch(self, user):
        return self.patch(
            viewname='rest_api:user-detail', args=(user.pk,),
            data={'username': TEST_USER_2_USERNAME_EDITED}
        )

    def test_user_edit_via_patch_no_access(self):
        user = self._create_user()
        response = self._request_user_edit_via_patch(user=user)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_2_USERNAME)

    def test_user_edit_via_patch_with_access(self):
        user = self._create_user()
        self.grant_access(permission=permission_user_edit, obj=user)
        response = self._request_user_edit_via_patch(user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_2_USERNAME_EDITED)

    def _request_user_edit_via_patch_with_extra_data(self, user, group):
        return self.patch(
            viewname='rest_api:user-detail', args=(user.pk,),
            data={'groups_pk_list': '{}'.format(group.pk)}
        )

    def test_user_edit_add_groups_via_patch_no_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()

        response = self._request_user_edit_via_patch_with_extra_data(
            user=user, group=group
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_2_USERNAME)

        self.assertQuerysetEqual(
            user.groups.all(), ()
        )

    def test_user_edit_add_groups_via_patch_with_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        self.grant_access(permission=permission_user_edit, obj=user)
        response = self._request_user_edit_via_patch_with_extra_data(
            user=user, group=group
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_2_USERNAME)

        self.assertQuerysetEqual(
            user.groups.all(), (repr(group),)
        )

    # User delete

    def _request_user_delete(self, user):
        return self.delete(
            viewname='rest_api:user-detail', args=(user.pk,)
        )

    def test_user_delete_no_access(self):
        user = self._create_user()
        response = self._request_user_delete(user=user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(get_user_model().objects.filter(pk=user.pk).exists())

    def test_user_delete_with_access(self):
        user = self._create_user()
        self.grant_access(permission=permission_user_delete, obj=user)
        response = self._request_user_delete(user=user)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(get_user_model().objects.filter(pk=user.pk).exists())

    # User view

    def _request_user_group_view(self, user):
        return self.get(
            viewname='rest_api:users-group-list', args=(user.pk,)
        )

    def test_user_group_list_no_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        user.groups.add(group)
        response = self._request_user_group_view(user=user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_group_list_with_user_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        user.groups.add(group)
        self.grant_access(permission=permission_user_view, obj=user)
        response = self._request_user_group_view(user=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_user_group_list_with_group_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        user.groups.add(group)
        self.grant_access(permission=permission_group_view, obj=group)
        response = self._request_user_group_view(user=user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_group_list_with_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        user.groups.add(group)
        self.grant_access(permission=permission_user_view, obj=user)
        self.grant_access(permission=permission_group_view, obj=group)
        response = self._request_user_group_view(user=user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def _request_user_group_add(self, user, group):
        return self.post(
            viewname='rest_api:users-group-list', args=(user.pk,), data={
                'group_pk_list': '{}'.format(group.pk)
            }
        )

    def test_user_group_add_no_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        response = self._request_user_group_add(user=user, group=group)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user.refresh_from_db()
        self.assertEqual(group.user_set.first(), None)

    def test_user_group_add_with_user_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        self.grant_access(permission=permission_user_edit, obj=user)
        response = self._request_user_group_add(user=user, group=group)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # FIXME: Should this endpoint return a 201 or a 200 since
        # the user is being edited and there is not resource creation
        # happening.
        user.refresh_from_db()
        self.assertEqual(group.user_set.first(), None)

    def test_user_group_add_with_group_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        self.grant_access(permission=permission_group_view, obj=group)
        response = self._request_user_group_add(user=user, group=group)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # FIXME: Should this endpoint return a 201 or a 200 since
        # the user is being edited and there is not resource creation
        # happening.
        user.refresh_from_db()
        self.assertEqual(group.user_set.first(), None)

    def test_user_group_add_with_access(self):
        group = Group.objects.create(name=TEST_GROUP_2_NAME)
        user = self._create_user()
        self.grant_access(permission=permission_user_edit, obj=user)
        self.grant_access(permission=permission_group_view, obj=group)
        response = self._request_user_group_add(user=user, group=group)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # FIXME: Should this endpoint return a 201 or a 200 since
        # the user is being edited and there is not resource creation
        # happening.
        user.refresh_from_db()
        self.assertEqual(group.user_set.first(), user)


class UserManagementGroupAPITestCase(BaseAPITestCase):
    def setUp(self):
        super(UserManagementGroupAPITestCase, self).setUp()
        self.login_user()

    def _request_group_create(self):
        return self.post(
            viewname='rest_api:group-list', data={
                'name': TEST_GROUP_2_NAME
            }
        )

    def test_group_create_no_permission(self):
        response = self._request_group_create()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(
            TEST_GROUP_2_NAME in list(Group.objects.values_list('name', flat=True))
        )

    def test_group_create_with_permission(self):
        self.grant_permission(permission=permission_group_create)
        response = self._request_group_create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            TEST_GROUP_2_NAME in list(Group.objects.values_list('name', flat=True))
        )

    def _request_group_edit_via_patch(self):
        return self.patch(
            viewname='rest_api:group-detail', args=(self.group.pk,),
            data={
                'name': TEST_GROUP_2_NAME_EDITED
            }
        )

    def test_group_edit_via_patch_no_access(self):
        self.group = Group.objects.create(name=TEST_GROUP_2_NAME)
        response = self._request_group_edit_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.group.refresh_from_db()
        self.assertEqual(self.group.name, TEST_GROUP_2_NAME)

    def test_group_edit_via_patch_with_access(self):
        self.group = Group.objects.create(name=TEST_GROUP_2_NAME)
        self.grant_access(permission=permission_group_edit, obj=self.group)
        response = self._request_group_edit_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group.refresh_from_db()
        self.assertEqual(self.group.name, TEST_GROUP_2_NAME_EDITED)

    def _request_group_delete(self):
        return self.delete(
            viewname='rest_api:group-detail', args=(self.group.pk,)
        )

    def test_group_delete_no_access(self):
        self.group = Group.objects.create(name=TEST_GROUP_2_NAME)
        response = self._request_group_delete()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            TEST_GROUP_2_NAME in list(Group.objects.values_list('name', flat=True))
        )

    def test_group_delete_with_access(self):
        self.group = Group.objects.create(name=TEST_GROUP_2_NAME)
        self.grant_access(permission=permission_group_delete, obj=self.group)
        response = self._request_group_delete()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            TEST_GROUP_2_NAME in list(Group.objects.values_list('name', flat=True))
        )
