from importlib import import_module
import logging

from django.apps import apps
from django.utils.encoding import force_text

logger = logging.getLogger(name=__name__)


class AppsModuleLoaderMixin:
    # __loader_module_sets is used to avoid double imports, it should not
    # be modified by the user.
    __loader_module_sets = {}

    # _loader_module_name must be set to the module name that is to be
    # uploaded by the class mixin.
    _loader_module_name = None

    @classmethod
    def load_modules(cls):
        # This set keeps track of what apps have already been processed.
        cls.__loader_module_sets.setdefault(cls._loader_module_name, set())

        for app in apps.get_app_configs():
            if app not in cls.__loader_module_sets[cls._loader_module_name]:
                try:
                    import_module('{}.{}'.format(app.name, cls._loader_module_name))
                except ImportError as exception:
                    # Determine which errors during import should be ignored
                    # and which are serious enough to raise.
                    non_fatal_messages = (
                        'No module named {module_name}'.format(
                            module_name=cls._loader_module_name
                        ),
                        'No module named \'{app_label}.{module_name}\''.format(
                            app_label=app.name, module_name=cls._loader_module_name
                        )
                    )
                    if force_text(s=exception) not in non_fatal_messages:
                        logger.error(
                            'Error importing %s %s.py file; %s', app.name,
                            cls._loader_module_name, exception, exc_info=True
                        )
                        raise
                finally:
                    cls.__loader_module_sets[cls._loader_module_name].add(app)
