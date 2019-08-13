from __future__ import absolute_import, unicode_literals

from furl import furl

from django.conf import settings
from django.contrib.auth.views import (
    INTERNAL_RESET_SESSION_TOKEN, INTERNAL_RESET_URL_TOKEN,
)
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.smart_settings.classes import Namespace
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.tests.literals import TEST_USER_PASSWORD_EDITED

from ..settings import setting_maximum_session_length

from .literals import TEST_EMAIL_AUTHENTICATION_BACKEND
from .mixins import UserPasswordViewTestMixin


class CurrentUserViewTestCase(GenericViewTestCase):
    def test_current_user_set_password_view(self):
        new_password = 'new_password_123'

        response = self.post(
            viewname='authentication:password_change_view', data={
                'old_password': self._test_case_user.cleartext_password,
                'new_password1': new_password,
                'new_password2': new_password
            }, follow=True
            # The follow is to test this and the next redirect, two tests in
            # one.
        )
        self.assertEqual(response.status_code, 200)

        self._test_case_user.refresh_from_db()
        self.assertTrue(self._test_case_user.check_password(raw_password=new_password))


class UserLoginTestCase(GenericViewTestCase):
    """
    Test that users can login via the supported authentication methods
    """
    authenticated_url = reverse(viewname='common:home')
    # Unquote directly until furl 2.1.0 is released which will include
    # the tostr() argument query_dont_quote=True
    # TODO: Remove after release and update to furl 2.1.0
    authentication_url = urlunquote_plus(
        furl(
            path=reverse(settings.LOGIN_URL), args={
                'next': authenticated_url
            }
        ).tostr()
    )
    auto_login_user = False
    create_test_case_superuser = True

    def setUp(self):
        super(UserLoginTestCase, self).setUp()
        Namespace.invalidate_cache_all()

    def _request_authenticated_view(self):
        return self.get(path=self.authenticated_url)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_non_authenticated_request(self):
        response = self._request_authenticated_view()
        self.assertRedirects(
            response=response, expected_url=self.authentication_url
        )

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_login(self):
        logged_in = self.login(
            username=self._test_case_superuser.username,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertTrue(logged_in)
        response = self._request_authenticated_view()
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_login(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            logged_in = self.login(
                username=self._test_case_superuser.username,
                password=self._test_case_superuser.cleartext_password
            )
            self.assertFalse(logged_in)

            logged_in = self.login(
                email=self._test_case_superuser.email,
                password=self._test_case_superuser.cleartext_password
            )
            self.assertTrue(logged_in)

            response = self._request_authenticated_view()
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_login_via_views(self):
        response = self._request_authenticated_view()
        self.assertRedirects(
            response=response, expected_url=self.authentication_url
        )

        response = self.post(
            viewname=settings.LOGIN_URL, data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password
            }
        )
        response = self._request_authenticated_view()
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_login_via_views(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            response = self._request_authenticated_view()
            self.assertRedirects(
                response=response, expected_url=self.authentication_url
            )

            response = self.post(
                viewname=settings.LOGIN_URL, data={
                    'email': self._test_case_superuser.email,
                    'password': self._test_case_superuser.cleartext_password
                }, follow=True
            )
            self.assertEqual(response.status_code, 200)

            response = self._request_authenticated_view()
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_remember_me(self):
        response = self.post(
            viewname=settings.LOGIN_URL, data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password,
                'remember_me': True
            }, follow=True
        )

        response = self._request_authenticated_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.client.session.get_expiry_age(),
            setting_maximum_session_length.value
        )
        self.assertFalse(self.client.session.get_expire_at_browser_close())

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_dont_remember_me(self):
        response = self.post(
            viewname=settings.LOGIN_URL, data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password,
                'remember_me': False
            }, follow=True
        )

        response = self._request_authenticated_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.client.session.get_expire_at_browser_close())

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_remember_me(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            response = self.post(
                viewname=settings.LOGIN_URL, data={
                    'email': self._test_case_superuser.email,
                    'password': self._test_case_superuser.cleartext_password,
                    'remember_me': True
                }, follow=True
            )

            response = self._request_authenticated_view()
            self.assertEqual(response.status_code, 200)

            self.assertEqual(
                self.client.session.get_expiry_age(),
                setting_maximum_session_length.value
            )
            self.assertFalse(self.client.session.get_expire_at_browser_close())

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_dont_remember_me(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            response = self.post(
                viewname=settings.LOGIN_URL, data={
                    'email': self._test_case_superuser.email,
                    'password': self._test_case_superuser.cleartext_password,
                    'remember_me': False
                }
            )

            response = self._request_authenticated_view()
            self.assertEqual(response.status_code, 200)

            self.assertTrue(self.client.session.get_expire_at_browser_close())

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_password_reset(self):
        self.logout()
        response = self.post(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_superuser.email,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        email_parts = mail.outbox[0].body.replace('\n', '').split('/')
        uidb64 = email_parts[-3]
        token = email_parts[-2]

        # Add the token to the session
        session = self.client.session
        session[INTERNAL_RESET_SESSION_TOKEN] = token
        session.save()

        new_password = 'new_password_123'
        response = self.post(
            viewname='authentication:password_reset_confirm_view',
            kwargs={'uidb64': uidb64, 'token': INTERNAL_RESET_URL_TOKEN}, data={
                'new_password1': new_password,
                'new_password2': new_password
            }
        )

        self.assertNotIn(INTERNAL_RESET_SESSION_TOKEN, self.client.session)

        self._test_case_superuser.refresh_from_db()
        self.assertTrue(self._test_case_superuser.check_password(new_password))

    def test_username_login_redirect(self):
        TEST_REDIRECT_URL = reverse(viewname='common:about_view')

        response = self.post(
            path='{}?next={}'.format(
                reverse(settings.LOGIN_URL), TEST_REDIRECT_URL
            ), data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password,
                'remember_me': False
            }, follow=True
        )

        self.assertEqual(response.redirect_chain, [(TEST_REDIRECT_URL, 302)])


class UserViewTestCase(UserPasswordViewTestMixin, GenericViewTestCase):
    def test_user_set_password_view_no_access(self):
        self._create_test_user()

        password_hash = self.test_user.password

        response = self._request_test_user_password_set_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

    def test_user_set_password_view_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        password_hash = self.test_user.password

        response = self._request_test_user_password_set_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)

    def test_user_multiple_set_password_view_no_access(self):
        self._create_test_user()
        password_hash = self.test_user.password

        response = self._request_test_user_password_set_multiple_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

    def test_user_multiple_set_password_view_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        password_hash = self.test_user.password

        response = self._request_test_user_password_set_multiple_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)
