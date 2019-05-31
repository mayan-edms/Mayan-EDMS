from __future__ import unicode_literals

from importlib import import_module
import logging

from django.apps import apps
from django.utils import six
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class FieldClass(object):
    _registry = {}

    @staticmethod
    def initialize():
        for app in apps.get_app_configs():
            try:
                import_module('{}.form_fields'.format(app.name))
            except ImportError as exception:
                if force_text(exception) not in ('No module named form_fields', 'No module named \'{}.form_fields\''.format(app.name)):
                    logger.error(
                        'Error importing %s queues.py file; %s', app.name,
                        exception
                    )
                    raise

        FieldClass.update()

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def update(cls):
        FieldChoice = apps.get_model(
            app_label='forms', model_name='FieldChoice'
        )

        for field in cls.all():
            FieldChoice.objects.update_or_create(
                dotted_path=field.dotted_path, defaults={
                    'label': field.label
                }
            )

    def __init__(self, dotted_path, label):
        self.dotted_path = dotted_path
        self.label = label

        self.__class__._registry[self.dotted_path] = self

    def validate(self):
        try:
            import_string(dotted_path=self.dotted_path)
        except Exception as exception:
            logger.critical(
                'Exception validating field entry %s; %s', self.label, exception,
                exc_info=True
            )
            raise
