from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from ..tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from .literals import (
    TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_USERNAME,
    TEST_USER_USERNAME_EDITED
)


class UserManagementAPITestCase(APITestCase):
    """
    Test the document type API endpoints
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

    def test_user_create_with_group(self):
        group_1 = Group.objects.create(name='test group 1')

        response = self.client.post(
            reverse('rest_api:user-list'), data={
                'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME,
                'groups_pk_list': '{}'.format(group_1.pk)
            }
        )

        self.assertEqual(response.status_code, 201)

        user = get_user_model().objects.get(pk=response.data['id'])
        self.assertEqual(user.username, TEST_USER_USERNAME)
        self.assertQuerysetEqual(user.groups.all(), (repr(group_1),))

    def test_user_create_with_groups(self):
        group_1 = Group.objects.create(name='test group 1')
        group_2 = Group.objects.create(name='test group 2')

        response = self.client.post(
            reverse('rest_api:user-list'), data={
                'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME,
                'groups_pk_list': '{},{}'.format(group_1.pk, group_2.pk)
            }
        )

        self.assertEqual(response.status_code, 201)

        user = get_user_model().objects.get(pk=response.data['id'])
        self.assertEqual(user.username, TEST_USER_USERNAME)
        self.assertQuerysetEqual(
            user.groups.all().order_by('name'), (repr(group_1), repr(group_2))
        )

    def test_user_create_login(self):
        response = self.client.post(
            reverse('rest_api:user-list'), data={
                'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME,
            }
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            self.client.login(
                username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
            )
        )

    def test_user_create_login_password_change(self):
        response = self.client.post(
            reverse('rest_api:user-list'), data={
                'email': TEST_USER_EMAIL, 'password': 'bad_password',
                'username': TEST_USER_USERNAME,
            }
        )

        self.assertEqual(response.status_code, 201)

        self.assertFalse(
            self.client.login(
                username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
            )
        )

        user = get_user_model().objects.get(pk=response.data['id'])

        response = self.client.patch(
            reverse('rest_api:user-detail', args=(user.pk,)), data={
                'password': TEST_USER_PASSWORD,
            }
        )

        self.assertTrue(
            self.client.login(
                username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
            )
        )

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

    def test_user_edit_remove_groups_via_patch(self):
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )
        group_1 = Group.objects.create(name='test group 1')
        user.groups.add(group_1)

        response = self.client.patch(
            reverse('rest_api:user-detail', args=(user.pk,)),
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertQuerysetEqual(
            user.groups.all().order_by('name'), (repr(group_1),)
        )

    def test_user_edit_add_groups_via_patch(self):
        user = get_user_model().objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD,
            username=TEST_USER_USERNAME
        )
        group_1 = Group.objects.create(name='test group 1')

        response = self.client.patch(
            reverse('rest_api:user-detail', args=(user.pk,)),
            data={'groups_pk_list': '{}'.format(group_1.pk)}
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertQuerysetEqual(
            user.groups.all().order_by('name'), (repr(group_1),)
        )

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
