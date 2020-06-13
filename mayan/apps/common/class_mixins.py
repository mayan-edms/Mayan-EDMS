from importlib import import_module
import logging

from django.apps import apps
from django.utils.encoding import force_text

logger = logging.getLogger(name=__name__)


class AppsModuleLoaderMixin:
    _loader_module_name = None
    _loader_module_sets = {}

    @classmethod
    def load_modules(cls):
        cls._loader_module_sets.setdefault(cls._loader_module_name, set())

        for app in apps.get_app_configs():
            if app not in cls._loader_module_sets[cls._loader_module_name]:
                try:
                    import_module('{}.{}'.format(app.name, cls._loader_module_name))
                except ImportError as exception:
                    non_fatal_messages = (
                        'No module named {module_name}'.format(module_name=cls._loader_module_name),
                        'No module named \'{app_label}.{module_name}\''.format(app_label=app.name, module_name=cls._loader_module_name)
                    )
                    if force_text(exception) not in non_fatal_messages:
                        logger.error(
                            'Error importing %s %s.py file; %s', app.name,
                            cls._loader_module_name, exception
                        )
                        raise
                finally:
                    cls._loader_module_sets[cls._loader_module_name].add(app)
