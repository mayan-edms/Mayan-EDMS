from furl import furl

from django.conf import settings
from django.contrib.auth import authenticate
from django.test import override_settings
from django.urls import reverse
from django.utils.http import urlunquote_plus

from mayan.apps.smart_settings.classes import SettingNamespace
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import AuthenticationBackend

from .literals import (
    PATH_AUTHENTICATION_BACKEND_EMAIL, PATH_AUTHENTICATION_BACKEND_USERNAME
)
from .mixins import LoginViewTestMixin


class AuthenticationBackendTestCase(LoginViewTestMixin, GenericViewTestCase):
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

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_EMAIL)
    def test_email_authentication_backend(self):
        AuthenticationBackend.cls_initialize()

        user = authenticate(
            username=self._test_case_superuser.email,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertEqual(user, self._test_case_superuser)

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME)
    def test_username_authentication_backend(self):
        AuthenticationBackend.cls_initialize()

        user = authenticate(
            username=self._test_case_superuser.username,
            password=self._test_case_superuser.cleartext_password
        )
        self.assertEqual(user, self._test_case_superuser)
