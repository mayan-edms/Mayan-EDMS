from mayan.apps.databases.classes import BaseBackend

from .settings import (
    setting_authentication_backend, setting_authentication_backend_arguments
)


class AuthenticationBackend(BaseBackend):
    _loader_module_name = 'authentication_backends'

    @classmethod
    def get_instance(cls):
        authentication_backend_class = cls.get(
            name=setting_authentication_backend.value
        )
        return authentication_backend_class(
            **setting_authentication_backend_arguments.value
        )

    def get_form_list(self):
        return self.form_list


class AuthenticationBackendRememberMeMixin:
    def __init__(self, **kwargs):
        self.maximum_session_length = kwargs.pop('maximum_session_length')
        super().__init__(**kwargs)

    def login(self, form_list=None, kwargs=None, request=None):
        kwargs = kwargs or {}
        remember_me = kwargs.get('remember_me')

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
