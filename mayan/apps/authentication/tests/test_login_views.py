from furl import furl

from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.events import event_user_edited

from ..classes import AuthenticationBackend
from ..events import event_user_logged_in, event_user_logged_out

from .literals import (
    PATH_AUTHENTICATION_BACKEND_EMAIL, PATH_AUTHENTICATION_BACKEND_USERNAME,
)
from .mixins import LoginViewTestMixin, LogoutViewTestMixin


class LoginTestCase(LoginViewTestMixin, GenericViewTestCase):
    """
    Test that users can login via the supported authentication methods.
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

    def test_non_authenticated_request(self):
        self._clear_events()

        response = self._request_authenticated_view()
        self.assertRedirects(
            response=response, expected_url=self.authentication_url
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL)
    def test_login_view_with_email(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_email()
        self.assertEqual(response.status_code, 302)

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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL)
    def test_login_view_with_email_and_dont_remember_me(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_email(
            extra_data={'remember_me': False}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get_expire_at_browser_close())

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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL)
    def test_login_view_with_email_and_remember_me(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_email(
            extra_data={'remember_me': True}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session.get_expiry_age(),
            AuthenticationBackend.cls_get_instance().maximum_session_length
        )
        self.assertFalse(self.client.session.get_expire_at_browser_close())

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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME)
    def test_login_view_with_username(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_username()
        self.assertEqual(response.status_code, 302)

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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME)
    def test_login_view_with_username_and_dont_remember_me(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_username(
            extra_data={'remember_me': False}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get_expire_at_browser_close())

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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME)
    def test_login_view_with_username_and_remember_me(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_username(
            extra_data={'remember_me': True}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session.get_expiry_age(),
            AuthenticationBackend.cls_get_instance().maximum_session_length
        )
        self.assertFalse(self.client.session.get_expire_at_browser_close())

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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME)
    def test_login_view_redirect_with_username(self):
        AuthenticationBackend.cls_initialize()

        TEST_REDIRECT_URL = reverse(viewname='common:about_view')

        self._clear_events()

        response = self._request_login_view_with_username(
            query={'next': TEST_REDIRECT_URL}, follow=True
        )
        self.assertEqual(response.status_code, 200)
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


class LogoutViewTestCase(LogoutViewTestMixin, GenericViewTestCase):
    def test_logout_view(self):
        self._clear_events()

        request = self._request_logout_view()
        self.assertEqual(request.status_code, 302)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_logged_out.id)
