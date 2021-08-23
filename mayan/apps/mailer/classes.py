import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin

__all__ = ('MailerBackend',)
logger = logging.getLogger(name=__name__)


class MailerBackendMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if not new_class.__module__ == 'mayan.apps.mailer.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class MailerBackendBase(AppsModuleLoaderMixin):
    """
    Base class for the mailing backends. This class is mainly a wrapper
    for other Django backends that adds a few metadata to specify the
    fields it needs to be instanciated at runtime.

    The fields attribute is a list of dictionaries with the format:
    {
        'name': ''  # Field internal name
        'label': ''  # Label to show to users
        'class': ''  # Field class to use. Field classes are Python dot
                       paths to Django's form fields.
        'initial': ''  # Field initial value
        'default': ''  # Default value.
    }
    """
    class_path = ''  # Dot path to the actual class that will handle the mail
    fields = {}

    @classmethod
    def get_class_fields(cls):
        backend_field_list = getattr(cls, 'fields', {}).keys()
        return getattr(cls, 'class_fields', backend_field_list)


class MailerBackend(MailerBackendBase, metaclass=MailerBackendMetaclass):
    _loader_module_name = 'mailers'

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry

    @classmethod
    def get_choices(cls):
        return sorted(
            [
                (
                    key, backend.label
                ) for key, backend in cls.get_all().items()
            ], key=lambda x: x[1]
        )


class NullBackend(MailerBackend):
    label = _('Null backend')
