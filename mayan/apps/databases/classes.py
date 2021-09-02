import logging

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin

logger = logging.getLogger(name=__name__)


class BackendMetaclass(type):
    __exclude_module = None
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if not new_class.__module__ == __name__:
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class BaseBackend(AppsModuleLoaderMixin, metaclass=BackendMetaclass):
    @classmethod
    def get(cls, name):
        return cls.__class__._registry[name]

    @classmethod
    def get_all(cls):
        return cls.__class__._registry

    @classmethod
    def get_choices(cls):
        choices = [
            (key, backend.label) for key, backend in cls.get_all().items()
        ]

        choices.sort(key=lambda x: x[1])

        return choices

    def __init__(self, model_instance_id, **kwargs):
        self.model_instance_id = model_instance_id
        self.kwargs = kwargs
