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
    form_class = AuthenticationFormUsernamePassword
    #form_list = (AuthenticationFormUsernamePassword,)
    form_list = ()

    def identify(self, request, form_list=None, kwargs=None):
        #return list(form_list)[0].get_user()
        return get_user_model().objects.get(
            pk=request.session['_multi_factor_user_id']
        )


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

    #def identify(self, form_list, request, kwargs=None):
    #    return list(form_list)[0].get_user()
    def identify(self, request, form_list=None, kwargs=None):
        #return list(form_list)[0].get_user()
        return get_user_model().get(pk=self.request._multi_factor_user_id)

    def initialize(self):
        settings.AUTHENTICATION_BACKENDS = (
            get_class_full_name(klass=EmailModelBackend),
        )
