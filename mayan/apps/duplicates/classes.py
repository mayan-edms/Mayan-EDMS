import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.classes import StoredBaseBackend

__all__ = ('DuplicateBackend',)
logger = logging.getLogger(name=__name__)


class DuplicateBackend(StoredBaseBackend):
    _backend_app_label = 'duplicates'
    _backend_model_name = 'StoredDuplicateBackend'
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
