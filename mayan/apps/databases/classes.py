import logging

from django.core.exceptions import ImproperlyConfigured

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.utils import get_class_full_name

logger = logging.getLogger(name=__name__)


class BackendMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )

        # Filter class hierarchy. Select only the class with App loader
        # support. This means that is the class meant to work as the
        # app's backend class.
        base_backend_class = [
            parent for parent in new_class.mro() if '_loader_module_name' in parent.__dict__ and parent._loader_module_name
        ]

        # No more than one app backend class should be returned.
        if len(base_backend_class) > 1:
            raise ImproperlyConfigured(
                'More than one backend parent class was returned. Should be '
                'only one.'
            )

        if base_backend_class:
            base_backend_class = base_backend_class[0]

            if base_backend_class != new_class:
                # Get this new child class full name, to be used as the
                # registry key.
                new_class_full_name = get_class_full_name(klass=new_class)

                # Initialize the app backend class registry.
                base_backend_class._registry.setdefault(
                    base_backend_class, {}
                )

                # Add the new child class to the app backend class registry.
                base_backend_class._registry[
                    base_backend_class
                ][new_class_full_name] = new_class

        return new_class


class BaseBackend(AppsModuleLoaderMixin, metaclass=BackendMetaclass):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry.get(cls, {})[name]

    @classmethod
    def get_all(cls):
        return cls._registry.get(cls, ())

    @classmethod
    def get_choices(cls):
        choices = [
            (key, backend.label) for key, backend in cls.get_all().items()
        ]

        choices.sort(key=lambda x: x[1])

        return choices


class ModelBaseBackend(BaseBackend):
    def __init__(self, model_instance_id, **kwargs):
        self.model_instance_id = model_instance_id
        self.kwargs = kwargs
