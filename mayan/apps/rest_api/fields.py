from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class DynamicSerializerField(serializers.ReadOnlyField):
    serializers = {}

    @classmethod
    def add_serializer(cls, klass, serializer_class):
        if isinstance(klass, str):
            klass = import_string(dotted_path=klass)

        if isinstance(serializer_class, str):
            serializer_class = import_string(dotted_path=serializer_class)

        cls.serializers[klass] = serializer_class

    def to_representation(self, value):
        for klass, serializer_class in self.serializers.items():
            if isinstance(value, klass):
                return serializer_class(
                    context={
                        'format': self.context['format'],
                        'request': self.context['request']
                    }
                ).to_representation(instance=value)

        return _('Unable to find serializer class for: %s') % value
