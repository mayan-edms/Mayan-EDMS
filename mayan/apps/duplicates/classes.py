import logging

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.classes import BaseBackend

__all__ = ('DuplicateBackend',)
logger = logging.getLogger(name=__name__)


class DuplicateBackend(BaseBackend):
    _loader_module_name = 'duplicate_backends'

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

    def _process(self, document):
        pass
