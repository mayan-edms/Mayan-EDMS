from django.core.exceptions import ValidationError
from django.utils.text import format_lazy

from mayan.apps.common.class_mixins import AppsModuleLoaderMixin
from mayan.apps.common.classes import PropertyHelper
from mayan.apps.common.literals import EMPTY_LABEL


class DocumentMetadataHelper(PropertyHelper):
    @staticmethod
    @property
    def constructor(*args, **kwargs):
        return DocumentMetadataHelper(*args, **kwargs)

    def get_result(self, name):
        return self.instance.metadata.get(metadata_type__name=name).value


class MetadataLookup:
    _registry = []

    @classmethod
    def get_as_context(cls):
        result = {}
        for entry in cls._registry:
            try:
                result[entry.name] = entry.value()
            except TypeError:
                result[entry.name] = entry.value

        return result

    @classmethod
    def get_as_help_text(cls):
        result = []
        for entry in cls._registry:
            result.append(
                '{{{{ {0} }}}} = "{1}"'.format(entry.name, entry.description)
            )

        return ' '.join(result)

    def __init__(self, description, name, value):
        self.description = description
        self.name = name
        self.value = value
        self.__class__._registry.append(self)


class MetadataTypeParserMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if new_class.__module__ != 'mayan.apps.metadata.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class MetadataTypeValidatorMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if new_class.__module__ != 'mayan.apps.metadata.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class MetadataTypeModuleMixin(AppsModuleLoaderMixin):
    arguments = ()

    @classmethod
    def get_all(cls):
        return cls._registry.values()

    @classmethod
    def get_choices(cls, add_blank=False):
        choices = [
            (entry.get_import_path(), entry.get_full_label()) for entry in cls.get_all()
        ]
        choices.sort(key=lambda x: x[1])

        if add_blank:
            choices.insert(0, (None, EMPTY_LABEL))

        return choices

    @classmethod
    def get_import_path(cls):
        return cls.__module__ + '.' + cls.__name__

    @classmethod
    def get_full_label(cls):
        arguments_string = ', '.join(cls.arguments)
        if arguments_string:
            arguments_template = '(arguments: {})'.format(arguments_string)
        else:
            arguments_template = ''

        return format_lazy(
            '{label} {arguments_template}'.format(
                label=cls.label, arguments_template=arguments_template
            )
        )

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def execute(self, input_data):
        raise NotImplementedError


class MetadataParser(MetadataTypeModuleMixin, metaclass=MetadataTypeParserMetaclass):
    _loader_module_name = 'metadata_parsers'

    def parse(self, input_data):
        try:
            return self.execute(input_data)
        except Exception as exception:
            raise ValidationError(exception)


class MetadataValidator(MetadataTypeModuleMixin, metaclass=MetadataTypeValidatorMetaclass):
    _loader_module_name = 'metadata_validators'

    def validate(self, input_data):
        try:
            self.execute(input_data)
        except Exception as exception:
            raise ValidationError(exception)
