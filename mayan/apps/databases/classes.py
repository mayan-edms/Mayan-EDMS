import logging

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_text
from django.utils.functional import classproperty
from django.utils.translation import ugettext_lazy as _

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
    _backend_identifier = 'backend_class_path'
    _registry = {}

    @classproperty
    def backend_class_path(cls):
        return cls.get_class_path()

    @classproperty
    def backend_id(cls):
        return getattr(cls, cls._backend_identifier)

    @classmethod
    def get(cls, name):
        return cls._registry.get(cls, {})[name]

    @classmethod
    def get_all(cls):
        return list(cls._registry.get(cls, {}).values())

    @classmethod
    def get_choices(cls):
        choices = [
            (
                backend.backend_id, backend.label
            ) for backend in cls.get_all()
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
        registry_key = klass.backend_id

        # Add the new child class to the app backend class registry.
        cls._registry[cls][registry_key] = klass


class ModelAttribute:
    _class_registry = []
    _model_registry = {}

    @classmethod
    def get_all_choices_for(cls, model):
        result = []

        for klass in cls._class_registry:
            klass_choices = klass.get_choices_for(model=model)
            if klass_choices:
                result.append(
                    (klass.class_label, klass_choices)
                )

        return result

    @classmethod
    def get_choices_for(cls, model):
        return sorted(
            (
                (entry.name, entry.get_display()) for entry in cls.get_for(model=model)
            ), key=lambda x: x[1]
        )

    @classmethod
    def get_for(cls, model):
        try:
            return cls._model_registry[cls.class_name][model]
        except KeyError:
            # We were passed a model instance, try again using the model of
            # the instance.

            # If we are already in the model class, exit with an error.
            if model.__class__ == models.base.ModelBase:
                return []

            return cls.get_for(model=type(model))

    @classmethod
    def register(cls, klass):
        cls._class_registry.append(klass)

    def __init__(self, model, name, label=None, description=None):
        self.model = model
        self.label = label
        self.name = name
        self.description = description
        self._model_registry.setdefault(self.class_name, {})
        self._model_registry[self.class_name].setdefault(model, [])
        self._model_registry[self.class_name][model].append(self)

    def get_display(self, show_name=False):
        if self.description:
            return '{} - {}'.format(
                self.name if show_name else self.label, self.description
            )
        else:
            return force_text(s=self.name if show_name else self.label)


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


class ModelField(ModelAttribute):
    class_label = _('Model fields')
    class_name = 'field'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._final_model_verbose_name = None

        if not self.label:
            self.label = self.get_field_attribute(
                attribute='verbose_name'
            )
            if self.label != self._final_model_verbose_name:
                self.label = '{}, {}'.format(
                    self._final_model_verbose_name, self.label
                )

        if not self.description:
            self.description = self.get_field_attribute(
                attribute='help_text'
            )

    def get_field_attribute(self, attribute, model=None, field_name=None):
        if not model:
            model = self.model

        if not field_name:
            field_name = self.name

        parts = field_name.split('__')
        if len(parts) > 1:
            return self.get_field_attribute(
                model=model._meta.get_field(parts[0]).related_model,
                field_name='__'.join(parts[1:]), attribute=attribute
            )
        else:
            self._final_model_verbose_name = model._meta.verbose_name
            return getattr(
                model._meta.get_field(field_name=field_name),
                attribute
            )


class ModelFieldRelated(ModelField):
    class_label = _('Model related fields')
    class_name = 'related_field'


class ModelProperty(ModelAttribute):
    class_label = _('Model properties')
    class_name = 'property'


class ModelReverseField(ModelField):
    class_label = _('Model reverse fields')
    class_name = 'reverse_field'

    def __init__(self, *args, **kwargs):
        super(ModelField, self).__init__(*args, **kwargs)
        self._final_model_verbose_name = None

        if not self.label:
            self.label = self.get_field_attribute(
                attribute='verbose_name_plural'
            )

    def get_field_attribute(self, attribute, model=None, field_name=None):
        if not model:
            model = self.model

        if not field_name:
            field_name = self.name

        return getattr(
            model._meta.get_field(field_name=field_name).related_model._meta,
            attribute
        )


class ModelQueryFields:
    _registry = {}

    @classmethod
    def get(cls, model):
        try:
            return cls._registry[model]
        except KeyError:
            ModelQueryFields(model=model)
            return cls.get(model=model)

    def __init__(self, model):
        self.model = model
        self.select_related_fields = []
        self.prefetch_related_fields = []
        self.__class__._registry[model] = self

    def add_select_related_field(self, field_name):
        if field_name in self.select_related_fields:
            raise ImproperlyConfigured(
                '"{}" model already has a "{}" query select related field.'.format(
                    self.model, field_name
                )
            )
        self.select_related_fields.append(field_name)

    def add_prefetch_related_field(self, field_name):
        if field_name in self.prefetch_related_fields:
            raise ImproperlyConfigured(
                '"{}" model already has a "{}" query prefetch related field.'.format(
                    self.model, field_name
                )
            )
        self.prefetch_related_fields.append(field_name)

    def get_queryset(self, manager_name=None):
        if manager_name:
            manager = getattr(self.model, manager_name)
        else:
            manager = self.model._meta.default_manager

        queryset = manager.all()

        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)

        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(
                *self.prefetch_related_fields
            )

        return queryset


class QuerysetParametersSerializer:
    @staticmethod
    def decompose(_model, _method_name, _manager_name=None, **kwargs):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        _manager_name = _manager_name or _model._meta.default_manager.name

        serialized_kwargs = []
        for name, value in kwargs.items():
            try:
                content_type = ContentType.objects.get_for_model(model=value)
            except AttributeError:
                """The value is not a model instance, pass it as-is."""
                serialized_kwargs.append(
                    {
                        'name': name,
                        'value': value
                    }
                )
            else:
                serialized_kwargs.append(
                    {
                        'name': name,
                        'content_type_id': content_type.pk,
                        'object_id': value.pk
                    }
                )

        return {
            'model_content_type_id': ContentType.objects.get_for_model(
                model=_model
            ).pk,
            'manager_name': _manager_name,
            'method_name': _method_name,
            'kwargs': serialized_kwargs
        }

    @staticmethod
    def rebuild(decomposed_queryset):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        model = ContentType.objects.get(
            pk=decomposed_queryset['model_content_type_id']
        ).model_class()

        queryset = getattr(model, decomposed_queryset['manager_name'])

        kwargs = {}

        for parameter in decomposed_queryset.get('kwargs', ()):
            if 'content_type_id' in parameter:
                content_type = ContentType.objects.get(
                    pk=parameter['content_type_id']
                )
                value = content_type.get_object_for_this_type(
                    pk=parameter['object_id']
                )
            else:
                value = parameter['value']

            kwargs[parameter['name']] = value

        return getattr(
            queryset, decomposed_queryset['method_name']
        )(**kwargs)


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


ModelAttribute.register(klass=ModelProperty)
ModelAttribute.register(klass=ModelField)
ModelAttribute.register(klass=ModelFieldRelated)
ModelAttribute.register(klass=ModelReverseField)
