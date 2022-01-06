from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from mayan.apps.databases.classes import BaseBackend

from .settings import (
    setting_authentication_backend, setting_authentication_backend_arguments
)


class AuthenticationBackend(BaseBackend):
    _loader_module_name = 'authentication_backends'
    form_list = ()
    login_form_class = None
    login_form_class_path = 'django.contrib.auth.forms.AuthenticationForm'

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

    def get_condition_dict(self):
        result = {}

        for form_index, form in enumerate(iterable=self.form_list):
            condition = getattr(form, 'condition', None)
            if condition:
                def condition_wrapper(authentication_backend):
                    # SessionWizard form condition method is hard coded
                    # to receive only the wizard instance. This wrapper
                    # allows passing also the `authentication_backend`.
                    def wrapper(wizard):
                        return condition(
                            authentication_backend=authentication_backend,
                            wizard=wizard
                        )

                    return wrapper

                result[str(form_index)] = condition_wrapper(
                    authentication_backend=self
                )

        return result

    def get_form_list(self):
        return self.form_list

    def get_login_form_class(self):
        if not self.login_form_class:
            if not self.login_form_class_path:
                raise ImproperlyConfigured(
                    'Must specify a `login_form_class` or a '
                    '`login_form_class_path`.'
                )
            else:
                return import_string(
                    dotted_path=self.login_form_class_path
                )
        else:
            return self.login_form_class

    def get_user(self, request, form_list=None, kwargs=None):
        """
        Required method to identify the user based on form and request data.
        """
        raise NotImplementedError

    def process(request, form_list=None, kwargs=None):
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
