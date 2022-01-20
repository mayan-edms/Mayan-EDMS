from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView
from django.test import override_settings

from ..classes import AuthenticationBackend
from ..literals import USER_IMPERSONATE_VARIABLE_ID

from .literals import PATH_AUTHENTICATION_BACKEND_USERNAME


class LoginViewTestMixin:
    def _request_authenticated_view(self):
        return self.get(path=self.authenticated_url)

    def _request_login_view(self, data, query=None, follow=False):
        default_data = {}

        default_data.update(data)

        return self.post(
            follow=follow, viewname=settings.LOGIN_URL, data=default_data,
            query=query
        )

    @override_settings(AUTHENTICATION_BACKEND=PATH_AUTHENTICATION_BACKEND_USERNAME)
    def _request_simple_login_view(self, follow=None, query=None):
        AuthenticationBackend.cls_initialize()

        data = {
            'username': self._test_case_user.username,
            'password': self._test_case_user.cleartext_password,
        }

        return self._request_login_view(data=data, follow=follow, query=query)

    def _request_login_view_with_email(self, extra_data=None):
        data = {
            'username': self._test_case_superuser.email,
            'password': self._test_case_superuser.cleartext_password,
        }

        if extra_data:
            data.update(extra_data)

        return self._request_login_view(data=data)

    def _request_login_view_with_username(
        self, extra_data=None, follow=None, query=None
    ):
        data = {
            'username': self._test_case_superuser.username,
            'password': self._test_case_superuser.cleartext_password,
        }

        if extra_data:
            data.update(extra_data)

        return self._request_login_view(data=data, follow=follow, query=query)

    def _request_multi_factor_authentication_view(
        self, data=None, query=None, follow=False
    ):
        default_data = {
            'multi_factor_authentication_view-current_step': '0'
        }

        default_data.update(data or {})

        return self.post(
            data=default_data, follow=follow, query=query,
            viewname='authentication:multi_factor_authentication_view'
        )


class LogoutViewTestMixin:
    def _request_logout_view(self):
        return self.post(viewname='authentication:logout_view')


class PasswordResetViewTestMixin:
    def _request_password_reset_confirm_view(self, new_password, uidb64):
        return self.post(
            viewname='authentication:password_reset_confirm_view',
            kwargs={
                'uidb64': uidb64,
                'token': PasswordResetConfirmView.reset_url_token
            }, data={
                'new_password1': new_password,
                'new_password2': new_password
            }
        )

    def _request_password_reset_get_view(self):
        return self.get(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_superuser.email,
            }
        )

    def _request_password_reset_post_view(self):
        return self.post(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_superuser.email,
            }
        )


class UserImpersonationViewTestMixin:
    def _impersonate_test_user(self):
        session = self.client.session
        session[USER_IMPERSONATE_VARIABLE_ID] = self.test_user.pk
        session.save()

    def _request_test_user_impersonate_end_view(self):
        return self.get(
            follow=True, viewname='authentication:user_impersonate_end'
        )

    def _request_test_user_impersonate_form_start_view(self):
        return self.post(
            follow=True, viewname='authentication:user_impersonate_form_start',
            data={
                'user_to_impersonate': self.test_user.pk
            }
        )

    def _request_test_user_impersonate_start_view(self):
        return self.post(
            follow=True, viewname='authentication:user_impersonate_start', kwargs={
                'user_id': self.test_user.pk
            }
        )


class UserPasswordViewTestMixin:
    def _request_test_user_password_set_view(self, password):
        return self.post(
            viewname='authentication:user_set_password', kwargs={
                'user_id': self.test_user.pk
            }, data={
                'new_password1': password, 'new_password2': password
            }
        )

    def _request_test_user_password_set_multiple_view(self, password):
        return self.post(
            viewname='authentication:user_multiple_set_password', data={
                'id_list': self.test_user.pk,
                'new_password1': password,
                'new_password2': password
            }
        )
