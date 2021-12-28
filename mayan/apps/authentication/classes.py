from mayan.apps.databases.classes import BaseBackend

from .literals import DEFAULT_MAXIMUM_SESSION_LENGTH


class AuthenticationBackend(BaseBackend):
    _loader_module_name = 'authentication_backends'

    def get_form_list(self):
        return self.form_list


class AuthenticationBackendRememberMeMixin:
    def __init__(self, **kwargs):
        self.maximum_session_length = kwargs.pop(
            'maximum_session_length', DEFAULT_MAXIMUM_SESSION_LENGTH
        )
        super().__init__(**kwargs)

    def login(self, cleaned_data, form_list, request):
        remember_me = cleaned_data.get('remember_me')

        # remember_me values:
        # True - long session
        # False - short session
        # None - Form has no remember_me value and we let the session
        # expiration default.

        if remember_me is True:
            request.session.set_expiry(
                self.maximum_session_length
            )
        elif remember_me is False:
            request.session.set_expiry(0)
