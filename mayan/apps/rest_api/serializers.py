from __future__ import absolute_import, unicode_literals

from rest_framework import serializers


class LazyExtraFieldsSerializerMixin(object):
    _registry = {}

    @classmethod
    def add_field(cls, dotted_path, field_name, field):
        cls._registry.setdefault(dotted_path, {})
        cls._registry[dotted_path][field_name] = field

    @classmethod
    def get_fields_for(cls, dotted_path):
        return cls._registry.get(dotted_path, {}).items()

    def get_dotted_path(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)

    def get_extra_fields(self):
        return self.__class__.get_fields_for(dotted_path=self.get_dotted_path())

    def __init__(self, *args, **kwargs):
        for field_name, field in self.get_extra_fields():
            self._declared_fields[field_name] = field
            self.__class__.Meta.fields += (field_name,)

        super(LazyExtraFieldsSerializerMixin, self).__init__(*args, **kwargs)


class LazyExtraFieldsHyperlinkedModelSerializer(
    LazyExtraFieldsSerializerMixin, serializers.HyperlinkedModelSerializer
):
    pass
