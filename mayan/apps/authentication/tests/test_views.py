from furl import furl

from django.conf import settings
from django.contrib.auth.views import (
    INTERNAL_RESET_SESSION_TOKEN, INTERNAL_RESET_URL_TOKEN,
)
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.common.settings import setting_home_view
from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.events import event_user_edited
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.tests.literals import (
    TEST_USER_PASSWORD_EDITED
)

from ..events import (
    event_user_impersonation_ended, event_user_impersonation_started,
    event_user_logged_in
)
from ..literals import USER_IMPERSONATE_VARIABLE_DISABLE
from ..permissions import permission_users_impersonate
from ..settings import setting_maximum_session_length

from .literals import TEST_EMAIL_AUTHENTICATION_BACKEND
from .mixins import (
    UserImpersonationViewTestMixin, UserLoginTestMixin,
    UserPasswordViewTestMixin
)


class CurrentUserViewTestCase(GenericViewTestCase):
    def test_current_user_set_password_view(self):
        new_password = 'new_password_123'

        self._clear_events()

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
        self.assertTrue(
            self._test_case_user.check_password(raw_password=new_password)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class UserImpersonationViewTestCase(
    UserImpersonationViewTestMixin, GenericViewTestCase
):
    def test_user_impersonate_form_start_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_impersonate_form_start_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_form_start_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self._clear_events()

        response = self._request_test_user_impersonate_form_start_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_started.id)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self.test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_end_view_no_permission(self):
        self._create_test_user()

        self._impersonate_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self.test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.revoke_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self.expected_content_types = ('text/html; charset=utf-8',)

        self._clear_events()

        response = self._request_test_user_impersonate_end_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_end_view_with_access(self):
        self._create_test_user()

        self._impersonate_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self.test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('text/html; charset=utf-8',)

        self._clear_events()

        response = self._request_test_user_impersonate_end_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_ended.id)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_session_impersonate_set_with_acess(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self._impersonate_test_user()

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self.test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_session_impersonate_unset_with_access(self):
        self._create_test_user()
        self.grant_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self._impersonate_test_user()

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(
            viewname='rest_api:user-current', query={
                USER_IMPERSONATE_VARIABLE_DISABLE: ''
            }
        )
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_ended.id)

    def test_user_impersonate_start_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_impersonate_start_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_start_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_users_impersonate
        )

        self._clear_events()

        response = self._request_test_user_impersonate_start_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_started.id)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self.test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class UserLoginTestCase(UserLoginTestMixin, GenericViewTestCase):
    """
    Test that users can login via the supported authentication methods
    """
    authenticated_url = reverse(viewname='common:home')
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
        super().setUp()
        SettingNamespace.invalidate_cache_all()

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_non_authenticated_request(self):
        self._clear_events()

        response = self._request_authenticated_view()
        self.assertRedirects(
            response=response, expected_url=self.authentication_url
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_login(self):
        logged_in = self.login(
            username=self._test_case_superuser.username,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertTrue(logged_in)

        self._clear_events()

        response = self._request_authenticated_view()
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

            self._clear_events()

            response = self._request_authenticated_view()
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)

            events = self._get_test_events()
            self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_login_via_views(self):
        self._clear_events()

        response = self._request_authenticated_view()
        self.assertRedirects(
            response=response, expected_url=self.authentication_url
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self._clear_events()

        response = self.post(
            viewname=settings.LOGIN_URL, data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password
            }
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_user_edited.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_superuser)
        self.assertEqual(events[1].target, self._test_case_superuser)
        self.assertEqual(events[1].verb, event_user_logged_in.id)

        self._clear_events()

        response = self._request_authenticated_view()
        # We didn't get redirected to the login URL
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_login_via_views(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            self._clear_events()

            response = self._request_authenticated_view()
            self.assertRedirects(
                response=response, expected_url=self.authentication_url
            )

            events = self._get_test_events()
            self.assertEqual(events.count(), 0)

            self._clear_events()

            response = self.post(
                viewname=settings.LOGIN_URL, data={
                    'email': self._test_case_superuser.email,
                    'password': self._test_case_superuser.cleartext_password
                }, follow=True
            )
            self.assertEqual(response.status_code, 200)

            events = self._get_test_events()
            self.assertEqual(events.count(), 2)

            self.assertEqual(events[0].action_object, None)
            self.assertEqual(events[0].actor, self._test_case_superuser)
            self.assertEqual(events[0].target, self._test_case_superuser)
            self.assertEqual(events[0].verb, event_user_edited.id)

            self.assertEqual(events[1].action_object, None)
            self.assertEqual(events[1].actor, self._test_case_superuser)
            self.assertEqual(events[1].target, self._test_case_superuser)
            self.assertEqual(events[1].verb, event_user_logged_in.id)

            self._clear_events()

            response = self._request_authenticated_view()
            # We didn't get redirected to the login URL
            self.assertEqual(response.status_code, 200)

            events = self._get_test_events()
            self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_remember_me(self):
        self._clear_events()

        response = self.post(
            viewname=settings.LOGIN_URL, data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password,
                'remember_me': True
            }, follow=True
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_user_edited.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_superuser)
        self.assertEqual(events[1].target, self._test_case_superuser)
        self.assertEqual(events[1].verb, event_user_logged_in.id)

        self._clear_events()

        response = self._request_authenticated_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.client.session.get_expiry_age(),
            setting_maximum_session_length.value
        )
        self.assertFalse(self.client.session.get_expire_at_browser_close())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_username_dont_remember_me(self):
        self._clear_events()

        response = self.post(
            viewname=settings.LOGIN_URL, data={
                'username': self._test_case_superuser.username,
                'password': self._test_case_superuser.cleartext_password,
                'remember_me': False
            }, follow=True
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_user_edited.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_superuser)
        self.assertEqual(events[1].target, self._test_case_superuser)
        self.assertEqual(events[1].verb, event_user_logged_in.id)

        self._clear_events()

        response = self._request_authenticated_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.client.session.get_expire_at_browser_close())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_remember_me(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            self._clear_events()

            response = self.post(
                viewname=settings.LOGIN_URL, data={
                    'email': self._test_case_superuser.email,
                    'password': self._test_case_superuser.cleartext_password,
                    'remember_me': True
                }, follow=True
            )

            events = self._get_test_events()
            self.assertEqual(events.count(), 2)

            self.assertEqual(events[0].action_object, None)
            self.assertEqual(events[0].actor, self._test_case_superuser)
            self.assertEqual(events[0].target, self._test_case_superuser)
            self.assertEqual(events[0].verb, event_user_edited.id)

            self.assertEqual(events[1].action_object, None)
            self.assertEqual(events[1].actor, self._test_case_superuser)
            self.assertEqual(events[1].target, self._test_case_superuser)
            self.assertEqual(events[1].verb, event_user_logged_in.id)

            self._clear_events()

            response = self._request_authenticated_view()
            self.assertEqual(response.status_code, 200)

            self.assertEqual(
                self.client.session.get_expiry_age(),
                setting_maximum_session_length.value
            )
            self.assertFalse(
                self.client.session.get_expire_at_browser_close()
            )

            events = self._get_test_events()
            self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='email')
    def test_email_dont_remember_me(self):
        with self.settings(AUTHENTICATION_BACKENDS=(TEST_EMAIL_AUTHENTICATION_BACKEND,)):
            self._clear_events()

            response = self.post(
                viewname=settings.LOGIN_URL, data={
                    'email': self._test_case_superuser.email,
                    'password': self._test_case_superuser.cleartext_password,
                    'remember_me': False
                }
            )

            events = self._get_test_events()
            self.assertEqual(events.count(), 2)

            self.assertEqual(events[0].action_object, None)
            self.assertEqual(events[0].actor, self._test_case_superuser)
            self.assertEqual(events[0].target, self._test_case_superuser)
            self.assertEqual(events[0].verb, event_user_edited.id)

            self.assertEqual(events[1].action_object, None)
            self.assertEqual(events[1].actor, self._test_case_superuser)
            self.assertEqual(events[1].target, self._test_case_superuser)
            self.assertEqual(events[1].verb, event_user_logged_in.id)

            self._clear_events()

            response = self._request_authenticated_view()
            self.assertEqual(response.status_code, 200)

            self.assertTrue(self.client.session.get_expire_at_browser_close())

            events = self._get_test_events()
            self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_LOGIN_METHOD='username')
    def test_password_reset(self):
        self.logout()
        self._clear_events()

        response = self._request_password_reset_post_view()

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self._clear_events()

        response = self.post(
            viewname='authentication:password_reset_confirm_view',
            kwargs={'uidb64': uidb64, 'token': INTERNAL_RESET_URL_TOKEN},
            data={
                'new_password1': new_password,
                'new_password2': new_password
            }
        )

        self.assertNotIn(INTERNAL_RESET_SESSION_TOKEN, self.client.session)

        self._test_case_superuser.refresh_from_db()
        self.assertTrue(
            self._test_case_superuser.check_password(new_password)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_username_login_redirect(self):
        TEST_REDIRECT_URL = reverse(viewname='common:about_view')

        self._clear_events()

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_user_edited.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self._test_case_superuser)
        self.assertEqual(events[1].target, self._test_case_superuser)
        self.assertEqual(events[1].verb, event_user_logged_in.id)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=False)
    def test_password_reset_disable_false_get_view(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_get_view()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=True)
    def test_password_reset_disable_true_get_view(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_get_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(viewname=setting_home_view.value)
        )

        self.assertEqual(len(mail.outbox), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=False)
    def test_password_reset_disable_false_post_view(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_post_view()

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, setting_home_view.value)

        self.assertEqual(len(mail.outbox), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=True)
    def test_password_reset_disable_true_post_view(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_post_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(viewname=setting_home_view.value)
        )

        self.assertEqual(len(mail.outbox), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class UserViewTestCase(UserPasswordViewTestMixin, GenericViewTestCase):
    def test_user_set_password_view_no_permission(self):
        self._create_test_user()

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_set_password_view_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_user_multiple_set_password_view_no_permission(self):
        self._create_test_user()
        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_multiple_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_multiple_set_password_view_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_multiple_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)
