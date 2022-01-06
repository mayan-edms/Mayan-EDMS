from furl import furl

from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.authentication.classes import AuthenticationBackend
from mayan.apps.authentication.events import event_user_logged_in
from mayan.apps.authentication.tests.mixins import LoginViewTestMixin
from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.events import event_user_edited
from mayan.apps.views.http import URL

from .literals import (
    PATH_AUTHENTICATION_BACKEND_EMAIL_OTP,
    PATH_AUTHENTICATION_BACKEND_USERNAME_OTP
)
from .mixins import AuthenticationOTPTestMixin


class LoginOTPTestCase(
    AuthenticationOTPTestMixin, LoginViewTestMixin, GenericViewTestCase
):
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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL_OTP)
    def test_login_view_with_email_no_otp(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_email()
        self.assertEqual(response.status_code, 302)

        response = self._request_multi_factor_authentication_view()
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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL_OTP)
    def test_login_view_with_email_with_otp(self):
        AuthenticationBackend.cls_initialize()

        self._enable_test_otp()

        self._clear_events()

        response = self._request_login_view_with_email()
        self.assertEqual(response.status_code, 302)

        response = self._request_multi_factor_authentication_view(
            data={
                '0-token': self._test_token
            }
        )
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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME_OTP)
    def test_login_view_with_username_no_otp(self):
        AuthenticationBackend.cls_initialize()

        self._clear_events()

        response = self._request_login_view_with_username()
        self.assertEqual(response.status_code, 302)

        response = self._request_multi_factor_authentication_view()
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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME_OTP)
    def test_login_view_with_username_with_otp(self):
        AuthenticationBackend.cls_initialize()

        self._enable_test_otp()

        self._clear_events()

        response = self._request_login_view_with_username()
        self.assertEqual(response.status_code, 302)

        response = self._request_multi_factor_authentication_view(
            data={
                '0-token': self._test_token
            }
        )
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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME_OTP)
    def test_login_view_redirect_with_username_and_otp(self):
        AuthenticationBackend.cls_initialize()

        TEST_REDIRECT_URL = reverse(viewname='common:about_view')
        self._enable_test_otp()

        self._clear_events()

        response = self._request_login_view_with_username(
            follow=True, query={'next': TEST_REDIRECT_URL}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.redirect_chain, [
                (
                    URL(
                        path=reverse(
                            viewname='authentication:multi_factor_authentication_view'
                        ), query={'next': TEST_REDIRECT_URL}
                    ).to_string(), 302
                ),
            ]
        )

        response = self._request_multi_factor_authentication_view(
            data={
                '0-token': self._test_token
            }, follow=True, query={'next': TEST_REDIRECT_URL}
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
