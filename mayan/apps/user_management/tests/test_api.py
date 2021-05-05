from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_group_created, event_group_edited, event_user_created,
    event_user_edited
)
from ..permissions import (
    permission_group_create, permission_group_delete,
    permission_group_edit, permission_group_view,
    permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)

from .mixins import (
    GroupAPIViewTestMixin, GroupTestMixin, GroupUserAPIViewTestMixin,
    UserAPIViewTestMixin, UserGroupAPIViewTestMixin
)


class GroupAPITestCase(
    GroupAPIViewTestMixin, GroupTestMixin, BaseAPITestCase
):
    def test_group_create_api_view_no_permission(self):
        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Group.objects.count(), group_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_group_create)

        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Group.objects.count(), group_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_created.id)

    def test_group_delete_api_view_no_permission(self):
        self._create_test_group()
        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Group.objects.count(), group_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_delete_api_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_delete
        )
        group_count = Group.objects.count()

        self._clear_events()

        response = self._request_test_group_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Group.objects.count(), group_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_detail_api_view_no_permission(self):
        self._create_test_group()

        self._clear_events()

        response = self._request_test_group_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_detail_api_view_with_access(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )

        self._clear_events()

        response = self._request_test_group_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_group.id)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_edit_api_view_via_patch_no_permission(self):
        self._create_test_group()

        group_name = self.test_group.name

        self._clear_events()

        response = self._request_test_group_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, group_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_edit_api_view_via_patch_with_access(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        group_name = self.test_group.name

        self._clear_events()

        response = self._request_test_group_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_group.refresh_from_db()
        self.assertNotEqual(self.test_group.name, group_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)

    def test_group_edit_api_view_via_put_no_permission(self):
        self._create_test_group()

        group_name = self.test_group.name

        self._clear_events()

        response = self._request_test_group_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, group_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_edit_api_view_via_put_with_access(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        group_name = self.test_group.name

        self._clear_events()

        response = self._request_test_group_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_group.refresh_from_db()
        self.assertNotEqual(self.test_group.name, group_name)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)

    def test_group_list_api_view_no_permission(self):
        self._create_test_group()

        self._clear_events()

        response = self._request_test_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_list_api_view_with_access(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )

        self._clear_events()

        response = self._request_test_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], self.test_group.id)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class GroupUserAPIViewTestCase(
    GroupTestMixin, GroupUserAPIViewTestMixin, BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()

    def test_group_user_add_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_group_user_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_user not in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_api_view_with_group_access(self):
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_user not in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_api_view_with_user_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_user not in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_add_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.test_user in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_user)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)

    def test_group_user_list_api_view_no_permission(self):
        self.test_user.groups.add(self.test_group)

        self._clear_events()

        response = self._request_test_group_user_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_list_api_view_with_group_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )

        self._clear_events()

        response = self._request_test_group_user_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_list_api_view_with_user_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(obj=self.test_user, permission=permission_user_view)

        self._clear_events()

        response = self._request_test_group_user_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_list_api_view_with_full_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )
        self.grant_access(obj=self.test_user, permission=permission_user_view)

        self._clear_events()

        response = self._request_test_group_user_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['username'], self.test_user.username
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_api_view_no_permission(self):
        self.test_user.groups.add(self.test_group)

        self._clear_events()

        response = self._request_test_group_user_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_user in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_api_view_with_group_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_user in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_api_view_with_user_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_user in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_user_remove_api_view_with_full_access(self):
        self.test_user.groups.add(self.test_group)

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_group_user_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.test_user in self.test_group.user_set.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_user)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_group)
        self.assertEqual(events[0].verb, event_group_edited.id)


class UserAPIViewTestCase(UserAPIViewTestMixin, BaseAPITestCase):
    def test_user_create_api_view_no_permission(self):
        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(get_user_model().objects.count(), user_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_user_create)

        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(get_user_model().objects.count(), user_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_created.id)

    def test_user_delete_api_view_no_permission(self):
        self._create_test_user()

        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(get_user_model().objects.count(), user_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_delete_api_view_with_access(self):
        self._create_test_user()
        self.grant_access(
            obj=self.test_user, permission=permission_user_delete
        )

        user_count = get_user_model().objects.count()

        self._clear_events()

        response = self._request_test_user_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(get_user_model().objects.count(), user_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_detail_api_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_detail_api_view_with_access(self):
        self._create_test_user()
        self.grant_access(
            obj=self.test_user, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_user_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['username'], self.test_user.username
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_edit_patch_api_view_no_permission(self):
        self._create_test_user()

        user_username = self.test_user.username

        self._clear_events()

        response = self._request_test_user_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, user_username)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_edit_patch_api_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        user_username = self.test_user.username

        self._clear_events()

        response = self._request_test_user_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.username, user_username)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_user_edit_put_api_view_no_permission(self):
        self._create_test_user()

        user_username = self.test_user.username

        self._clear_events()

        response = self._request_test_user_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, user_username)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_edit_put_api_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        user_username = self.test_user.username

        self._clear_events()

        response = self._request_test_user_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.username, user_username)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_user_password_change_api_view_no_permission(self):
        self._create_test_user()

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_password_change_api_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_change_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class UserGroupAPIViewTestCase(
    UserGroupAPIViewTestMixin, GroupTestMixin, BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_user()

    def test_user_group_list_api_view_no_permission(self):
        self.test_group.user_set.add(self.test_user)

        self._clear_events()

        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_list_api_view_with_user_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_user, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_list_api_view_with_group_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )

        self._clear_events()

        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_group_list_api_view_with_full_access(self):
        self.test_group.user_set.add(self.test_user)

        self.grant_access(
            obj=self.test_group, permission=permission_group_view
        )
        self.grant_access(
            obj=self.test_user, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_user_group_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['name'], self.test_group.name
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
