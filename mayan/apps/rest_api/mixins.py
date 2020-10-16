from django.core.exceptions import ImproperlyConfigured

from mayan.apps.views.mixins import ExternalObjectMixin


class AsymmetricSerializerViewMixin:
    _write_methods = ('PATCH', 'POST', 'PUT')
    read_serializer_class = None
    write_serializer_class = None

    def get_read_serializer_class(self):
        if not self.read_serializer_class:
            raise ImproperlyConfigured(
                'View {} must specify a read_serializer_class.'.format(
                    self.__class__.__name__
                )
            )
        else:
            return self.read_serializer_class

    def get_serializer_class(self):
        if getattr(self, 'serializer_class', None):
            raise ImproperlyConfigured(
                'View {} can not use AsymmetricSerializerViewMixin while '
                'also specifying a serializer_class.'.format(
                    self.__class__.__name__
                )
            )

        if self.request.method in self._write_methods:
            return self.get_write_serializer_class()
        else:
            return self.get_read_serializer_class()

    def get_write_serializer_class(self):
        if not self.write_serializer_class:
            raise ImproperlyConfigured(
                'View {} must specify a write_serializer_class.'.format(
                    self.__class__.__name__
                )
            )
        else:
            return self.write_serializer_class


class CreateOnlyFieldSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['view'].action != 'create':
            for field in getattr(self.Meta, 'create_only_fields', ()):
                self.fields.pop(field)


class ExternalObjectAPIViewMixin(ExternalObjectMixin):
    """
    Override get_external_object to use REST API get_object_or_404.
    """
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


class InstanceExtraDataAPIViewMixin:
    def perform_create(self, serializer):
        if hasattr(self, 'get_instance_extra_data'):
            serializer.validated_data['_instance_extra_data'] = self.get_instance_extra_data()

        return super().perform_create(serializer=serializer)

    def perform_destroy(self, instance):
        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                setattr(instance, key, value)

        return super().perform_destroy(instance=instance)

    def perform_update(self, serializer):
        if hasattr(self, 'get_instance_extra_data'):
            for key, value in self.get_instance_extra_data().items():
                serializer.validated_data[key] = value

        return super().perform_update(serializer=serializer)


class SerializerExtraContextAPIViewMixin:
    def get_serializer_extra_context(self):
        return {}

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.get_serializer_extra_context())
        return context


class SuccessHeadersAPIViewMixin:
    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
