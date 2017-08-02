from __future__ import unicode_literals

from importlib import import_module
import logging

from django.apps import apps
from django.utils import six
from django.utils.encoding import force_text

logger = logging.getLogger(__name__)


__ALL__ = ('QuotaBackend',)


class QuotaBackendMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super(QuotaBackendMetaclass, mcs).__new__(
            mcs, name, bases, attrs
        )
        if not new_class.__module__ == 'quotas.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class
            new_class.id = '{}.{}'.format(new_class.__module__, name)

        return new_class


class QuotaBackendBase(object):
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
    fields = ()


class QuotaBackend(six.with_metaclass(QuotaBackendMetaclass, QuotaBackendBase)):
    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return sorted(
            cls._registry.values(), key=lambda x: x.label
        )

    @classmethod
    def as_choices(cls):
        return [
            (
                backend.id, backend.label
            ) for backend in QuotaBackend.get_all()
        ]

    @staticmethod
    def initialize():
        for app in apps.get_app_configs():
            try:
                import_module('{}.quota_backends'.format(app.name))
            except ImportError as exception:
                if force_text(exception) != 'No module named quota_backends':
                    logger.error(
                        'Error importing %s quota_backends.py file; %s',
                        app.name, exception
                    )
