from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from ..settings import setting_login_method

TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_ADMIN_PASSWORD = 'test_admin_password'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_EMAIL_AUTHENTICATION_BACKEND = 'authentication.auth.email_auth_backend.EmailAuthBackend'


class UserLoginTestCase(TestCase):
    """
    Test that users can login via the supported authentication methods
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.client = Client()

    def test_normal_behaviour(self):
        setting_login_method.value = 'username'
        response = self.client.get(reverse('documents:document_list'))
        self.assertRedirects(
            response, 'http://testserver/authentication/login/'
        )

    def test_username_login(self):
        setting_login_method.value = 'username'
        logged_in = self.client.login(
            username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse('documents:document_list'))
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    def test_email_login(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            setting_login_method.value = 'email'

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

    def test_username_login_via_views(self):
        setting_login_method.value = 'username'
        response = self.client.get(reverse('documents:document_list'))
        self.assertRedirects(
            response, 'http://testserver/authentication/login/'
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

    def test_email_login_via_views(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            setting_login_method.value = 'email'
            response = self.client.get(reverse('documents:document_list'))
            self.assertRedirects(
                response, 'http://testserver/authentication/login/'
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
