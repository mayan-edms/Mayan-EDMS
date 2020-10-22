from importlib import import_module
import logging

from django.apps import apps
from django.utils.encoding import force_text

logger = logging.getLogger(name=__name__)


class ModuleLoaderMixin(object):
    _loader_module_name = None

    @classmethod
    def initialize(cls):
        for app in apps.get_app_configs():
            try:
                import_module('{}.{}'.format(app.name, cls._loader_module_name))
            except ImportError as exception:
                if force_text(s=exception) not in ('No module named {module_name}', 'No module named \'{app_label}.{module_name}\''.format(app_label=app.name, module_name=cls._loader_module_name)):
                    logger.error(
                        'Error importing %s %s.py file; %s',
                        app.name, cls._loader_module_name, exception
                    )
                    raise
