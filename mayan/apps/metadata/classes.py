from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _


class DocumentMetadataHelper(object):
    @staticmethod
    @property
    def constructor(source_object):
        return DocumentMetadataHelper(source_object)

    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, name):
        try:
            return self.instance.metadata.get(metadata_type__name=name).value
        except ObjectDoesNotExist:
            raise AttributeError(
                _('\'metadata\' object has no attribute \'%s\'') % name
            )


class MetadataLookup(object):
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
