from mayan.apps.databases.classes import BaseBackend

from .settings import (
    setting_authentication_backend, setting_authentication_backend_arguments
)


class AuthenticationBackend(BaseBackend):
    _loader_module_name = 'authentication_backends'

    @classmethod
    def cls_get_instance(cls):
        authentication_backend_class = cls.get(
            name=setting_authentication_backend.value
        )
        return authentication_backend_class(
            **setting_authentication_backend_arguments.value
        )

    @classmethod
    def cls_initialize(cls):
        backend = cls.cls_get_instance()
        backend.initialize()

    def initialize(self):
        """
        Optional subclass initialization method.
        """

    def get_form_list(self):
        return self.form_list

    def identify(self, form_list, request, kwargs=None):
        """
        Required method to identify the user based on form and request data.
        """
        raise NotImplementedError

    def process(form_list=None, kwargs=None, request=None):
        """
        Optional method to do login related setup based on form data like
        session TTL.
        """


class AuthenticationBackendRememberMeMixin:
    def __init__(self, **kwargs):
        self.maximum_session_length = kwargs.pop('maximum_session_length')
        super().__init__(**kwargs)

    def process(self, form_list=None, kwargs=None, request=None):
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
