from __future__ import unicode_literals

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Manager
from django.db.models.query import QuerySet

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from mayan.apps.common.utils import resolve_attribute


class MultiKwargHyperlinkedIdentityField(HyperlinkedIdentityField):
    def __init__(self, *args, **kwargs):
        self.view_kwargs = kwargs.pop('view_kwargs', [])
        super(MultiKwargHyperlinkedIdentityField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Extends HyperlinkedRelatedField to allow passing more than one view
        keyword argument.
        ----
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        kwargs = {}
        for entry in self.view_kwargs:
            if 'lookup_field' in entry:
                kwargs[entry['lookup_url_kwarg']] = resolve_attribute(
                    obj=obj, attribute=entry['lookup_field']
                )

            if 'field_attribute' in entry:
                kwargs[entry['lookup_url_kwarg']] = resolve_attribute(
                    obj=self, attribute=entry['field_attribute']
                )

        return self.reverse(
            viewname=view_name, kwargs=kwargs, request=request, format=format
        )


class RestrictedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.source_model = kwargs.pop('source_model', None)
        self.source_permission = kwargs.pop('source_permission', None)
        self.source_permission_method = kwargs.pop(
            'source_permission_method', None
        )
        self.source_queryset = kwargs.pop('source_queryset', None)
        self.source_queryset_method = kwargs.pop(
            'source_queryset_method', None
        )
        super(RestrictedPrimaryKeyRelatedField, self).__init__(**kwargs)

    def get_queryset(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        queryset_method = self.source_queryset_method or 'get_{field_name}_queryset'.format(
            field_name=self.field_name
        )

        if self.source_model:
            queryset = self.source_model._meta.default_manager.all()
        elif self.source_queryset:
            queryset = self.source_queryset
            if isinstance(queryset, (QuerySet, Manager)):
                # Ensure queryset is re-evaluated whenever used.
                queryset = queryset.all()
        else:
            try:
                queryset = getattr(self.parent, method_name)()
            except AttributeError:
                raise ImproperlyConfigured(
                    'Need to provide a source_model, a '
                    'source_queryset, a source_queryset_method, or '
                    'a method named "get_{field_name}_queryset".'.format(
                        self.field_name
                    )
                )

        assert 'request' in self.context, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        request = self.context['request']

        permission_method = self.source_permission_method or 'get_{field_name}_permission'.format(
            field_name=self.field_name
        )

        if self.source_permission:
            permission = self.source_permission
        elif self.source_permission_method:
            permission = getattr(self.parent, permission_method)()
        else:
            permission = None

        if permission:
            return AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=request.user
            )
        else:
            return queryset
