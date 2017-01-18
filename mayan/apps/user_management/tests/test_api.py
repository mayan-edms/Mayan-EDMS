from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from ..tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from .literals import (
    TEST_GROUP_NAME, TEST_GROUP_NAME_EDITED, TEST_USER_EMAIL,
    TEST_USER_PASSWORD, TEST_USER_USERNAME, TEST_USER_USERNAME_EDITED
)


class UserManagementUserAPITestCase(APITestCase):
    """
    Test the user API endpoints
    """

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_user_create(self):
        response = self.client.post(
            reverse('rest_api:user-list'), data={
                'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME,
            }
        )

        self.assertEqual(response.status_code, 201)

        user = get_user_model().objects.get(pk=response.data['id'])
        self.assertEqual(user.username, TEST_USER_USERNAME)

    def test_user_edit_via_put(self):
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )

        response = self.client.put(
            reverse('rest_api:user-detail', args=(user.pk,)),
            data={'username': TEST_USER_USERNAME_EDITED}
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_USERNAME_EDITED)

    def test_user_edit_via_patch(self):
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )

        response = self.client.patch(
            reverse('rest_api:user-detail', args=(user.pk,)),
            data={'username': TEST_USER_USERNAME_EDITED}
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.username, TEST_USER_USERNAME_EDITED)

    def test_user_delete(self):
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )

        response = self.client.delete(
            reverse('rest_api:user-detail', args=(user.pk,))
        )

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=user.pk)

    def test_user_group_list(self):
        group = Group.objects.create(name=TEST_GROUP_NAME)
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )
        user.groups.add(group)

        response = self.client.get(
            reverse('rest_api:users-group-list', args=(user.pk,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'][0]['name'], TEST_GROUP_NAME)

    def test_user_group_add(self):
        group = Group.objects.create(name=TEST_GROUP_NAME)
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )

        response = self.client.post(
            reverse(
                'rest_api:users-group-list', args=(user.pk,)
            ), data={
                'group_pk_list': '{}'.format(group.pk)
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(group.user_set.first(), user)


class UserManagementGroupAPITestCase(APITestCase):
    """
    Test the groups API endpoints
    """

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_group_create(self):
        response = self.client.post(
            reverse('rest_api:group-list'), data={'name': TEST_GROUP_NAME}
        )

        self.assertEqual(response.status_code, 201)

        group = Group.objects.get(pk=response.data['id'])
        self.assertEqual(group.name, TEST_GROUP_NAME)

    def test_group_edit_via_put(self):
        group = Group.objects.create(name=TEST_GROUP_NAME)
        response = self.client.put(
            reverse('rest_api:group-detail', args=(group.pk,)), data={
                'name': TEST_GROUP_NAME_EDITED
            }
        )

        self.assertEqual(response.status_code, 200)

        group.refresh_from_db()
        self.assertEqual(group.name, TEST_GROUP_NAME_EDITED)

    def test_group_edit_via_patch(self):
        group = Group.objects.create(name=TEST_GROUP_NAME)
        response = self.client.patch(
            reverse('rest_api:group-detail', args=(group.pk,)), data={
                'name': TEST_GROUP_NAME_EDITED
            }
        )

        self.assertEqual(response.status_code, 200)

        group.refresh_from_db()
        self.assertEqual(group.name, TEST_GROUP_NAME_EDITED)

    def test_group_delete(self):
        group = Group.objects.create(name=TEST_GROUP_NAME)
        response = self.client.delete(
            reverse('rest_api:group-detail', args=(group.pk,))
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Group.objects.count(), 0)
