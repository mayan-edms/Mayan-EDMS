from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.test.client import Client

from organizations.tests.base import OrganizationTestCase
from user_management.tests.literals import (
    TEST_ADMIN_EMAIL, TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME
)

from .literals import TEST_EMAIL_AUTHENTICATION_BACKEND


class UserLoginTestCase(OrganizationTestCase):
    """
    Test that users can login via the supported authentication methods
    """

    def setUp(self):
        super(UserLoginTestCase, self).setUp()
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()

    def tearDown(self):
        super(UserLoginTestCase, self).tearDown()

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_normal_behaviour(self):
        response = self.client.get(reverse('documents:document_list'))
        self.assertRedirects(
            response,
            'http://testserver/authentication/login/?next=/documents/list/'
        )

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_login(self):
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse('documents:document_list'))
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_login(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            logged_in = self.client.login(
                username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
            )
            self.assertFalse(logged_in)

            logged_in = self.client.login(
                email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD
            )
            self.assertTrue(logged_in)

            response = self.client.get(reverse('documents:document_list'))
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_login_via_views(self):
        response = self.client.get(reverse('documents:document_list'))
        self.assertRedirects(
            response,
            'http://testserver/authentication/login/?next=/documents/list/'
        )

        response = self.client.post(
            reverse(settings.LOGIN_URL), {
                'username': TEST_ADMIN_USERNAME,
                'password': TEST_ADMIN_PASSWORD
            }
        )
        response = self.client.get(reverse('documents:document_list'))
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_login_via_views(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            response = self.client.get(reverse('documents:document_list'))
            self.assertRedirects(
                response,
                'http://testserver/authentication/login/?next=/documents/list/'
            )

            response = self.client.post(
                reverse(settings.LOGIN_URL), {
                    'email': TEST_ADMIN_EMAIL, 'password': TEST_ADMIN_PASSWORD
                }, follow=True
            )
            self.assertEqual(response.status_code, 200)

            response = self.client.get(reverse('documents:document_list'))
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)
