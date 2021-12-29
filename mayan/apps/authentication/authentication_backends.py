from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from mayan.apps.common.utils import get_class_full_name

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

    def identify(self, form_list, request, kwargs=None):
        return list(form_list)[0].get_user()


class EmailModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(email=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class AuthenticationBackendModelEmailPassword(
    AuthenticationBackendRememberMeMixin, AuthenticationBackend
):
    form_list = (AuthenticationFormEmailPassword,)

    def identify(self, form_list, request, kwargs=None):
        return list(form_list)[0].get_user()

    def initialize(self):
        settings.AUTHENTICATION_BACKENDS = (
            get_class_full_name(klass=EmailModelBackend),
        )
