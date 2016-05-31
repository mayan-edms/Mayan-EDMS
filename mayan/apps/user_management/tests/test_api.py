from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse

from rest_api.tests.base import GenericAPITestCase

from .literals import (
    TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_USERNAME,
    TEST_USER_USERNAME_EDITED
)


class UserManagementAPITestCase(GenericAPITestCase):
    """
    Test the document type API endpoints
    """

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

    def test_user_create_login(self):
        response = self.client.post(
            reverse('rest_api:user-list'), data={
                'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD,
                'username': TEST_USER_USERNAME,
            }
        )

        self.assertEqual(response.status_code, 201)

        get_user_model().objects.get(pk=response.data['id'])

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

    def test_document_type_edit_via_patch(self):
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

    def test_document_type_delete(self):
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
