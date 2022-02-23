import logging

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.utils import get_class_full_name

logger = logging.getLogger(name=__name__)


class BackendMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )

        base_backend_class = BackendMetaclass._get_base_backend_class(
            klass=new_class
        )

        _loader_module_name = getattr(new_class, '_loader_module_name')

        # Check if `_loader_module_name` is set as to not process the
        # metaclass.
        if _loader_module_name and base_backend_class:
            if base_backend_class != new_class:
                # Get this new child class full name, to be used as the
                # registry key.
                new_class_full_name = get_class_full_name(klass=new_class)
                if _loader_module_name in new_class_full_name:
                    # Only load classes defined in the loader module.
                    # This ensures miscellaneous classes like NullBackends
                    # are not registered.
                    base_backend_class.register(klass=new_class)

        return new_class

    @staticmethod
    def _get_base_backend_class(klass):
        # Filter class hierarchy. Select only the class with App loader
        # support. This means that is the class meant to work as the
        # app's backend class.
        base_backend_class = [
            parent for parent in klass.mro() if '_loader_module_name' in parent.__dict__ and parent._loader_module_name
        ]

        # No more than one app backend class should be returned.
        if len(base_backend_class) > 1:
            raise ImproperlyConfigured(
                'More than one backend parent class was returned. Should be '
                'only one.'
            )

        if base_backend_class:
            return base_backend_class[0]
        else:
            return None


class BaseBackend(AppsModuleLoaderMixin, metaclass=BackendMetaclass):
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry.get(cls, {})[name]

    @classmethod
    def get_all(cls):
        return cls._registry.get(cls, {})

    @classmethod
    def get_choices(cls):
        choices = [
            (
                backend_path, backend.label
            ) for backend_path, backend in cls.get_all().items()
        ]

        choices.sort(key=lambda x: x[1])

        return choices

    @classmethod
    def get_class_path(cls):
        return get_class_full_name(klass=cls)

    @classmethod
    def register(cls, klass):
        # Initialize the app backend class registry.
        cls._registry.setdefault(
            cls, {}
        )

        # Get this new child class full name, to be used as the
        # registry key.
        class_full_name = get_class_full_name(klass=klass)

        # Add the new child class to the app backend class registry.
        cls._registry[
            cls
        ][class_full_name] = klass


class ModelBaseBackend(BaseBackend):
    _backend_app_label = None
    _backend_model_name = None

    @classmethod
    def register(cls, klass):
        super().register(klass=klass)

    def get_model_instance(self):
        BackendModel = apps.get_model(
            app_label=self._backend_app_label,
            model_name=self._backend_model_name
        )

        return BackendModel.objects.get(pk=self.model_instance_id)

    def __init__(self, model_instance_id, **kwargs):
        self.model_instance_id = model_instance_id
        self.kwargs = kwargs


class StoredBaseBackend(BaseBackend):
    _backend_app_label = None
    _backend_model_name = None

    @classmethod
    def register(cls, klass):
        super().register(klass=klass)
        klass.get_model_instance()

    @classmethod
    def get_model_instance(cls):
        StoredBackendModel = apps.get_model(
            app_label=cls._backend_app_label,
            model_name=cls._backend_model_name
        )

        backend_path = get_class_full_name(klass=cls)

        instance, created = StoredBackendModel.objects.get_or_create(
            backend_path=backend_path
        )
        cls._backend_stored_model_id = instance.pk
        return instance

    def __init__(self, **kwargs):
        self.kwargs = kwargs
