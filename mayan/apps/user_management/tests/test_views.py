from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from common.tests.test_views import GenericViewTestCase

from ..permissions import (
    permission_user_delete, permission_user_edit, permission_user_view
)

from .literals import (
    TEST_USER_PASSWORD, TEST_USER_PASSWORD_EDITED, TEST_USER_USERNAME
)

TEST_USER_TO_DELETE_USERNAME = 'user_to_delete'


class UserManagementViewTestCase(GenericViewTestCase):
    def test_user_set_password_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_set_password', args=(self.user.pk,), data={
                'new_password_1': TEST_USER_PASSWORD_EDITED,
                'new_password_2': TEST_USER_PASSWORD_EDITED
            }
        )

        self.assertEqual(response.status_code, 403)

        self.client.logout()
        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD_EDITED
        )

        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 302)

    def test_user_set_password_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_edit.stored_permission)
        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_set_password', args=(self.user.pk,), data={
                'new_password_1': TEST_USER_PASSWORD_EDITED,
                'new_password_2': TEST_USER_PASSWORD_EDITED
            }, follow=True
        )

        self.assertContains(response, text='Successfull', status_code=200)

        self.client.logout()
        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD_EDITED
        )
        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 200)

    def test_user_multiple_set_password_view_no_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_multiple_set_password', data={
                'id_list': self.user.pk,
                'new_password_1': TEST_USER_PASSWORD_EDITED,
                'new_password_2': TEST_USER_PASSWORD_EDITED
            }
        )

        self.assertEqual(response.status_code, 403)

        self.client.logout()
        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD_EDITED
        )

        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 302)

    def test_user_multiple_set_password_view_with_permissions(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_edit.stored_permission)
        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_multiple_set_password', data={
                'id_list': self.user.pk,
                'new_password_1': TEST_USER_PASSWORD_EDITED,
                'new_password_2': TEST_USER_PASSWORD_EDITED
            }, follow=True
        )

        self.assertContains(response, text='Successfull', status_code=200)

        self.client.logout()
        self.client.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD_EDITED
        )
        response = self.get('common:current_user_details')

        self.assertEqual(response.status_code, 200)

    def test_user_delete_view_no_permissions(self):
        user = get_user_model().objects.create(
            username=TEST_USER_TO_DELETE_USERNAME
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_delete', args=(user.pk,)
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_user_delete_view_with_permissions(self):
        user = get_user_model().objects.create(
            username=TEST_USER_TO_DELETE_USERNAME
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_delete.stored_permission)
        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_delete', args=(user.pk,), follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_user_multiple_delete_view_no_permissions(self):
        user = get_user_model().objects.create(
            username=TEST_USER_TO_DELETE_USERNAME
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_multiple_delete', data={
                'id_list': user.pk
            }
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(get_user_model().objects.count(), 3)

    def test_user_multiple_delete_view_with_permissions(self):
        user = get_user_model().objects.create(
            username=TEST_USER_TO_DELETE_USERNAME
        )

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_user_delete.stored_permission)
        self.role.permissions.add(permission_user_view.stored_permission)

        response = self.post(
            'user_management:user_multiple_delete', data={
                'id_list': user.pk,
            }, follow=True
        )

        self.assertContains(response, text='deleted', status_code=200)
        self.assertEqual(get_user_model().objects.count(), 2)
