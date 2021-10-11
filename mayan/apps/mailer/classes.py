import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.classes import ModelBaseBackend

__all__ = ('MailerBackend',)
logger = logging.getLogger(name=__name__)


class MailerBackend(ModelBaseBackend):
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
    _loader_module_name = 'mailers'
    class_path = ''  # Dot path to the actual class that will handle the mail

    @classmethod
    def get_fields(cls):
        return getattr(cls, 'fields', {})

    @classmethod
    def get_field_order(cls):
        return getattr(cls, 'field_order', ())

    @classmethod
    def get_form_schema(cls):
        result = {
            'fields': cls.get_fields(),
            'field_order': cls.get_field_order(),
            'widgets': cls.get_widgets()
        }

        return result

    @classmethod
    def get_widgets(cls):
        return getattr(cls, 'widgets', {})


class NullBackend(MailerBackend):
    label = _('Null backend')
