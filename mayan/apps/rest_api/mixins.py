from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured

from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.settings import api_settings

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.mixins import ExternalObjectMixin


class CreateOnlyFieldSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        super(CreateOnlyFieldSerializerMixin, self).__init__(*args, **kwargs)
        if self.context['view'].action != 'create':
            for field in getattr(self.Meta, 'create_only_fields', ()):
                self.fields.pop(field)


class ExternalObjectAPIViewSetMixin(ExternalObjectMixin):
    """
    Override get_external_object to use REST API get_object_or_404.
    """
    def dispatch(self, *args, **kwargs):
        return super(ExternalObjectMixin, self).dispatch(*args, **kwargs)

    def get_serializer_extra_context(self):
        """
        Add the external object to the serializer context. Useful for the
        create action when there is no instance available.
        """
        result = {}
        if self.kwargs:
            result['external_object'] = self.get_external_object()

        return result

    def get_external_object(self, permission=None):
        return get_object_or_404(
            queryset=self.get_external_object_queryset_filtered(
                permission=permission
            ), **self.get_pk_url_kwargs()
        )


class ExternalObjectListSerializerMixin(object):
    """
    Mixin to allow serializers to get a restricted object list with minimal code.
    This mixin adds the follow class Meta options to a serializer:
        external_object_list_model
        external_object_list_permission
        external_object_list_queryset
        external_object_list_pk_field
        external_object_list_pk_list_field
        external_object_list_pk_type

    The source queryset can also be provided overriding the
    .get_external_object_list_queryset() method.
    """
    def __init__(self, *args, **kwargs):
        super(ExternalObjectListSerializerMixin, self).__init__(*args, **kwargs)
        self.external_object_list_options = getattr(self, 'Meta', None)
        self.external_object_list_options_defaults = {
            'external_object_list_pk_type': int
        }

    def filter_queryset(self, id_list, queryset):
        """
        Allow customizing the final filtering, used for object lists that are
        not a queryset like the Permission class.
        """
        return queryset.filter(pk__in=id_list)

    def get_external_object_list(self, permission=None):
        permission = permission or self.get_external_object_list_option(
            option_name='permission'
        )

        queryset = self.get_external_object_list_queryset()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.context['request'].user
            )

        pk_field = self.get_external_object_list_option(
            option_name='pk_field'
        )
        pk_list_field = self.get_external_object_list_option(
            option_name='pk_list_field'
        )

        if not pk_field and not pk_list_field:
            raise ImproperlyConfigured(
                'ExternalObjectListSerializerMixin requires a '
                'external_object_list_pk_field or a'
                'external_object_list_pk_list_field.'
            )

        if pk_field:
            pk_field_value = self.validated_data.get(pk_field)
        else:
            pk_field_value = None

        if pk_list_field:
            pk_list_field_value = self.validated_data.get(pk_list_field)
        else:
            pk_list_field = None

        if pk_field_value:
            id_list = (pk_field_value,)
        elif pk_list_field_value:
            id_list = (pk_list_field_value or '').split(',')
        else:
            id_list = ()

        pk_type = self.get_external_object_list_option(option_name='pk_type')

        if pk_type:
            result = []

            for pk in id_list:
                try:
                    result.append(pk_type(pk))
                except Exception as exception:
                    raise ValidationError(
                        {
                            api_settings.NON_FIELD_ERRORS_KEY: [
                                'Value "{}" is not of a valid type; {}'.format(pk, exception)
                            ]
                        }, code='invalid'
                    )

            id_list = result

        return self.filter_queryset(id_list=id_list, queryset=queryset)

    def get_external_object_list_option(self, option_name):
        full_option_name = 'external_object_list_{}'.format(option_name)

        return getattr(
            self.external_object_list_options, full_option_name,
            self.external_object_list_options_defaults.get(full_option_name)
        )

    def get_external_object_list_queryset(self):
        model = self.get_external_object_list_option(option_name='model')
        queryset = self.get_external_object_list_option(option_name='queryset')

        if model:
            queryset = model._meta.default_manager.all()
        elif queryset is not None:
            return queryset
        else:
            raise ImproperlyConfigured(
                'ExternalObjectListSerializerMixin requires a '
                'external_object_list_model or a external_object_list_queryset.'
            )

        return queryset


class ExternalObjectSerializerMixin(object):
    """
    Mixin to allow serializers to get a restricted object with minimal code.
    This mixin adds the follow class Meta options to a serializer:
        external_object_model
        external_object_permission
        external_object_queryset
        external_object_pk_field
        external_object_pk_type
    The source queryset can also be provided overriding the
    .get_external_object_queryset() method.
    """
    def __init__(self, *args, **kwargs):
        super(ExternalObjectSerializerMixin, self).__init__(*args, **kwargs)
        self.external_object_options = getattr(self, 'Meta', None)

    def get_external_object(self, as_queryset=False, permission=None):
        queryset = self.get_external_object_queryset()

        permission = self.get_external_object_permission() or permission
        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset,
                user=self.context['request'].user
            )

        pk_field = self.get_external_object_option('pk_field')

        if not pk_field:
            raise ImproperlyConfigured(
                'ExternalObjectSerializerMixin requires a '
                'external_object_pk_field.'
            )

        if pk_field:
            pk_field_value = self.get_initial().get(pk_field)
        else:
            pk_field_value = None

        pk_type = self.get_external_object_option('pk_type')

        if pk_field_value:
            if pk_type:
                try:
                    pk_field_value = pk_type(pk_field_value)
                except Exception as exception:
                    raise ValidationError(
                        {
                            pk_field: [exception]
                        }, code='invalid'
                    )

            try:
                # Test and trigger 404
                result = queryset.get(pk=pk_field_value)

                if as_queryset:
                    return queryset.filter(pk=pk_field_value)
                else:
                    return result
            except Exception as exception:
                raise ValidationError(
                    {
                        pk_field: [exception]
                    }, code='invalid'
                )

    def get_external_object_option(self, option_name):
        full_option_name = 'external_object_{}'.format(option_name)

        return getattr(
            self.external_object_options, full_option_name,
            None
        )

    def get_external_object_permission(self):
        return self.get_external_object_option('permission')

    def get_external_object_queryset(self):
        model = self.get_external_object_option('model')
        queryset = self.get_external_object_option('queryset')

        if model:
            queryset = model._meta.default_manager.all()
        elif queryset is not None:
            return queryset
        else:
            raise ImproperlyConfigured(
                'ExternalObjectListSerializerMixin requires a '
                'external_object_model or a external_object_queryset.'
            )

        return queryset


class SerializerExtraContextMixin(object):
    def get_serializer_extra_context(self):
        return {}

    def get_serializer_context(self):
        context = super(SerializerExtraContextMixin, self).get_serializer_context()
        context.update(self.get_serializer_extra_context())
        return context


class SuccessHeadersMixin(object):
    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
