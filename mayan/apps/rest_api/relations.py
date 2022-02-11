from django.apps import apps
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from mayan.apps.common.utils import resolve_attribute

from .field_mixins import AutoHelpTextLabelFieldMixin


class FilteredRelatedFieldMixin:
    def __init__(self, **kwargs):
        self.source_model = kwargs.pop('source_model', None)
        self.source_permission = kwargs.pop('source_permission', None)
        self.source_queryset = kwargs.pop('source_queryset', None)
        self.source_queryset_method = kwargs.pop('source_queryset_method', None)

        super().__init__(**kwargs)

    def get_queryset(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        if self.source_model:
            queryset = self.source_model._meta.default_manager.all()
        elif self.source_queryset is not None:
            queryset = self.source_queryset
            if isinstance(queryset, (QuerySet, Manager)):
                # Ensure queryset is re-evaluated whenever used.
                queryset = queryset.all()
        else:
            method_name = self.source_queryset_method or 'get_{}_queryset'.format(
                self.field_name
            )
            try:
                queryset = getattr(self.parent, method_name)()
            except AttributeError:
                raise ImproperlyConfigured(
                    'Need to provide a source_model, a '
                    'source_queryset, a source_queryset_method, or '
                    'a method named "%s".' % method_name
                )

        assert 'request' in self.context, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        request = self.context['request']

        if self.source_permission:
            return AccessControlList.objects.restrict_queryset(
                permission=self.source_permission, queryset=queryset,
                user=request.user
            )
        else:
            return queryset


class FilteredPrimaryKeyRelatedField(
    AutoHelpTextLabelFieldMixin, FilteredRelatedFieldMixin,
    serializers.PrimaryKeyRelatedField
):
    """PrimaryKeyRelatedField that allows runtime queryset filtering by ACL."""


class FilteredSimplePrimaryKeyRelatedField(
    AutoHelpTextLabelFieldMixin, FilteredRelatedFieldMixin,
    serializers.RelatedField
):
    """
    PrimaryKeyRelatedField that allows runtime queryset filtering by ACL
    and that only stores the primary key.
    """
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop('pk_field', 'pk')
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        kwargs = {
            self.pk_field: data
        }

        queryset = self.get_queryset()
        try:
            return getattr(queryset.get(**kwargs), self.pk_field)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return getattr(value, self.pk_field)


class MultiKwargHyperlinkedIdentityField(HyperlinkedIdentityField):
    def __init__(self, *args, **kwargs):
        self.view_kwargs = kwargs.pop('view_kwargs', [])
        super().__init__(*args, **kwargs)

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
            kwargs[entry['lookup_url_kwarg']] = resolve_attribute(
                obj=obj, attribute=entry['lookup_field']
            )

        return self.reverse(
            viewname=view_name, kwargs=kwargs, request=request, format=format
        )
