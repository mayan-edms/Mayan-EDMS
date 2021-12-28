from django.contrib.auth import login as auth_login

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

    def login(self, cleaned_data, form_list, request):
        auth_login(request, list(form_list)[0].get_user())

        return super().login(
            cleaned_data=cleaned_data, form_list=form_list, request=request
        )


class AuthenticationBackendEmailPassword(
    AuthenticationBackendRememberMeMixin, AuthenticationBackend
):
    form_list = (AuthenticationFormEmailPassword,)

    def login(self, cleaned_data, form_list, request):
        auth_login(request, list(form_list)[0].get_user())

        return super().login(
            cleaned_data=cleaned_data, form_list=form_list, request=request
        )
