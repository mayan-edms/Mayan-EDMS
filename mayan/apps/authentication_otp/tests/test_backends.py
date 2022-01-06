from furl import furl

from django.conf import settings
from django.contrib.auth import authenticate
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.authentication.classes import AuthenticationBackend
from mayan.apps.authentication.tests.mixins import LoginViewTestMixin
from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import GenericViewTestCase

from .literals import (
    PATH_AUTHENTICATION_BACKEND_EMAIL_OTP,
    PATH_AUTHENTICATION_BACKEND_USERNAME_OTP
)
from .mixins import AuthenticationOTPTestMixin


class AuthenticationOTPBackendTestCase(
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
    def test_authentication_backend_email_no_otp(self):
        AuthenticationBackend.cls_initialize()

        user = authenticate(
            username=self._test_case_superuser.email,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertEqual(user, self._test_case_superuser)

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL_OTP)
    def test_authentication_backend_email_with_otp(self):
        AuthenticationBackend.cls_initialize()

        self._enable_test_otp()

        user = authenticate(
            username=self._test_case_superuser.email,
            password=self._test_case_superuser.cleartext_password,
        )
        self.assertEqual(user, self._test_case_superuser)

        user = authenticate(
            factor_name='otp_token', otp_token=self._test_token,
            user=user
        )
        self.assertEqual(user, self._test_case_superuser)

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME_OTP)
    def test_authentication_backend_username_no_otp(self):
        AuthenticationBackend.cls_initialize()

        user = authenticate(
            username=self._test_case_superuser.username,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertEqual(user, self._test_case_superuser)

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME_OTP)
    def test_authentication_backend_username_with_otp(self):
        AuthenticationBackend.cls_initialize()

        self._enable_test_otp()

        user = authenticate(
            username=self._test_case_superuser.username,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertEqual(user, self._test_case_superuser)

        user = authenticate(
            factor_name='otp_token', otp_token=self._test_token,
            user=user
        )
        self.assertEqual(user, self._test_case_superuser)
