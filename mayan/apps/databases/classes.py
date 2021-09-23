import logging

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.utils import get_class_full_name

logger = logging.getLogger(name=__name__)


class BackendMetaclass(type):
    __exclude_module = None

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )

        new_class_full_name = get_class_full_name(klass=new_class)
        base_backend_full_name = '{}.{}'.format(__name__, 'BaseBackend')
        base_model_backend_full_name = '{}.{}'.format(__name__, 'ModelBaseBackend')

        if new_class_full_name not in (base_backend_full_name, base_model_backend_full_name):
            parents = [
                base for base in bases if isinstance(base, BackendMetaclass)
            ]

            if get_class_full_name(klass=new_class.__bases__[0]) not in (base_backend_full_name, base_model_backend_full_name):
                parent_class = parents[0]
                parent_class._registry.setdefault(parent_class, {})
                parent_class._registry[parent_class][new_class_full_name] = new_class

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
