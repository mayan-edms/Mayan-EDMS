import logging

from django.apps import apps
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin


__all__ = ('DuplicateBackend',)
logger = logging.getLogger(name=__name__)


class DuplicateBackendMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if not new_class.__module__ == 'mayan.apps.duplicates.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class DuplicateBackend(
    six.with_metaclass(DuplicateBackendMetaclass, AppsModuleLoaderMixin)
):
    _loader_module_name = 'duplicate_backends'

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry.items()

    @classmethod
    def get_choices(cls):
        return sorted(
            [
                (
                    key, backend.label
                ) for key, backend in cls.get_all().items()
            ], key=lambda x: x[1]
        )

    @classmethod
    def get_class_path(cls):
        for path, klass in cls.get_all().items():
            if klass is cls:
                return path

    @classmethod
    def verify(cls, document):
        """
        Method to check is the document has can be scanned for duplicates.
        Returns either a true (True or anything) or false value (False, None).
        """
        return True

    def __init__(self, model_instance_id, **kwargs):
        self.model_instance_id = model_instance_id
        self.kwargs = kwargs

    def get_model_instance(self):
        StoredDuplicateBackend = apps.get_model(
            app_label='duplicated', model_name='StoredDuplicateBackend'
        )
        return StoredDuplicateBackend.objects.get(pk=self.model_instance_id)

    def process(self, document):
        logger.info(
            'Starting processing document: %s', document
        )

        return self._process(document=document)

    def _process(self, document):
        raise NotImplementedError(
            'Your %s class has not defined the required '
            '_process() method.' % self.__class__.__name__
        )


class NullBackend(DuplicateBackend):
    label = _('Null backend')
