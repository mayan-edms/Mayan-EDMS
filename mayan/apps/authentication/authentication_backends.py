from django.contrib.auth import login as django_auth_login

from .classes import (
    AuthenticationBackend, AuthenticationBackendRememberMeMixin
)
from .forms import (
    AuthenticationFormEmailPassword, AuthenticationFormUsernamePassword
)


class AuthenticationBackendModelUsernamePassword(
    AuthenticationBackendRememberMeMixin, AuthenticationBackend
):
    form_list = (AuthenticationFormUsernamePassword,)

    def login(self, form_list, request, kwargs=None):
        django_auth_login(
            request=request, user=list(form_list)[0].get_user()
        )

        return super().login(
            form_list=form_list, request=request, kwargs=kwargs
        )


class AuthenticationBackendEmailPassword(
    AuthenticationBackendRememberMeMixin, AuthenticationBackend
):
    form_list = (AuthenticationFormEmailPassword,)

    def login(self, form_list, request, kwargs=None):
        django_auth_login(
            request=request, user=list(form_list)[0].get_user()
        )

        return super().login(
            form_list=form_list, request=request, kwargs=kwargs
        )
