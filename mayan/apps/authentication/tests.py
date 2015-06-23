from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from .settings import setting_login_method

TEST_ADMIN_EMAIL = 'admin@admin.com'
TEST_ADMIN_PASSWORD = 'test_admin_password'
TEST_ADMIN_USERNAME = 'test_admin'


class UserLoginTestCase(TestCase):
    """
    Test that users can login via the supported authentication methods
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)
        self.client = Client()

    def test_normal_behaviour(self):
        # TODO set setting_login_method to 'username'
        # setattr(authentication.settings, 'LOGIN_METHOD', 'username')
        response = self.client.get(reverse('documents:document_list'))
        self.assertRedirects(response, 'http://testserver/authentication/login/')

    def test_username_login(self):
        # TODO set setting_login_method to 'username'
        # setattr(authentication.settings, 'LOGIN_METHOD', 'username')
        logged_in = self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
        self.assertTrue(logged_in)
        response = self.client.get(reverse('documents:document_list'))
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    def test_email_login(self):
        with self.settings(COMMON_LOGIN_METHOD='email', AUTHENTICATION_BACKENDS=('authentication.auth.email_auth_backend.EmailAuthBackend',)):
            # TODO set setting_login_method to 'email'
            #setattr(authentication.settings, 'LOGIN_METHOD', 'email')
            logged_in = self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
            self.assertFalse(logged_in)

            logged_in = self.client.login(email=TEST_ADMIN_EMAIL, password=TEST_ADMIN_PASSWORD)
            self.assertTrue(logged_in)

            response = self.client.get(reverse('documents:document_list'))
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)

    def test_username_login_via_views(self):
        # TODO set setting_login_method to 'username'
        # setattr(authentication.settings, 'LOGIN_METHOD', 'username')
        response = self.client.get(reverse('documents:document_list'))
        self.assertRedirects(response, 'http://testserver/authentication/login/')

        response = self.client.post(settings.LOGIN_URL, {'username': TEST_ADMIN_USERNAME, 'password': TEST_ADMIN_PASSWORD}, follow=True)
        response = self.client.get(reverse('documents:document_list'))
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    def test_email_login_via_views(self):
        with self.settings(COMMON_LOGIN_METHOD='email', AUTHENTICATION_BACKENDS=('authentication.auth.email_auth_backend.EmailAuthBackend',)):
            # TODO set setting_login_method to 'email'
            #setattr(authentication.settings, 'LOGIN_METHOD', 'email')
            response = self.client.get(reverse('documents:document_list'))
            self.assertRedirects(response, 'http://testserver/authentication/login/')

            response = self.client.post(settings.LOGIN_URL, {'email': TEST_ADMIN_EMAIL, 'password': TEST_ADMIN_PASSWORD}, follow=True)
            response = self.client.get(reverse('documents:document_list'))
            self.assertEqual(response.status_code, 200)
