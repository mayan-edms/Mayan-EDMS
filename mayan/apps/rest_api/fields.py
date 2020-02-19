from __future__ import unicode_literals

from django.utils.module_loading import import_string
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.common.utils import resolve_attribute


class DynamicSerializerField(serializers.ReadOnlyField):
    serializers = {}

    @classmethod
    def add_serializer(cls, klass, serializer_class):
        if isinstance(klass, string_types):
            klass = import_string(klass)

        if isinstance(serializer_class, string_types):
            serializer_class = import_string(serializer_class)

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


class HyperlinkField(serializers.Field):
    lookup_field = 'pk'
    view_name = None

    def __init__(self, view_name=None, **kwargs):
        kwargs['read_only'] = True
        self.view_kwargs = kwargs.pop('view_kwargs', None)

        if view_name is not None:
            self.view_name = view_name
        assert self.view_name is not None, 'The `view_name` argument is required.'
        self.lookup_field = kwargs.pop('lookup_field', self.lookup_field)
        self.lookup_url_kwarg = kwargs.pop('lookup_url_kwarg', self.lookup_field)
        self.format = kwargs.pop('format', None)

        super(HyperlinkField, self).__init__(**kwargs)

    def get_attribute(self, instance):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return instance

    def to_representation(self, value):
        kwargs = {}

        if self.view_kwargs:
            for item in self.view_kwargs:
                kwargs[item['lookup_url_kwarg']] = resolve_attribute(
                    obj=value, attribute=item['lookup_field']
                )
        else:
            kwargs[self.lookup_url_kwarg] = getattr(value, self.lookup_field)

        return reverse(
            kwargs=kwargs, request=self.context.get('request'),
            viewname=self.view_name
        )
