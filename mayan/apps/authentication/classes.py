from mayan.apps.databases.classes import BaseBackend

from .settings import setting_maximum_session_length


class AuthenticationBackend(BaseBackend):
    _loader_module_name = 'authentication_backends'
    __exclude_modules = 'mayan.apps.authentication.classes'


class AuthenticationBackendRememberMeMixin:
    def login(self, cleaned_data, done_data, form_list, request):
        remember_me = cleaned_data.get('remember_me')

        # remember_me values:
        # True - long session
        # False - short session
        # None - Form has no remember_me value and we let the session
        # expiration default.

        if remember_me is True:
            request.session.set_expiry(
                setting_maximum_session_length.value
            )
        elif remember_me is False:
            request.session.set_expiry(0)

        return super().login(
            cleaned_data=cleaned_data, done_data=done_data,
            form_list=form_list, request=request
        )
