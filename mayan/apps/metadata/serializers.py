from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from mayan.apps.documents.serializers.document_serializers import (
    DocumentSerializer
)
from mayan.apps.documents.serializers.document_type_serializers import (
    DocumentTypeSerializer
)
from mayan.apps.rest_api.serializer_mixins import CreateOnlyFieldSerializerMixin
from mayan.apps.rest_api.relations import FilteredPrimaryKeyRelatedField

from .models import DocumentMetadata, DocumentTypeMetadataType, MetadataType
from .permissions import permission_document_metadata_add


class MetadataTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_field': 'pk', 'lookup_url_kwarg': 'metadata_type_id',
                'view_name': 'rest_api:metadatatype-detail'
            },
        }
        fields = (
            'default', 'id', 'label', 'lookup', 'name', 'parser', 'url',
            'validation'
        )
        model = MetadataType


class DocumentTypeMetadataTypeSerializer(serializers.HyperlinkedModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)
    metadata_type = MetadataTypeSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        fields = ('document_type', 'id', 'metadata_type', 'required', 'url')
        model = DocumentTypeMetadataType

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documenttypemetadatatype-detail', kwargs={
                'document_type_id': instance.document_type.pk,
                'metadata_type_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )


class NewDocumentTypeMetadataTypeSerializer(serializers.ModelSerializer):
    metadata_type_id = serializers.IntegerField(
        help_text=_('Primary key of the metadata type to be added.'),
        write_only=True
    )
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'metadata_type_id', 'required', 'url'
        )
        model = DocumentTypeMetadataType

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documenttypemetadatatype-detail', kwargs={
                'document_type_id': instance.document_type.pk,
                'metadata_type_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def validate(self, attrs):
        attrs['document_type'] = self.context['document_type']
        attrs['metadata_type'] = MetadataType.objects.get(
            pk=attrs.pop('metadata_type_id')
        )

        instance = DocumentTypeMetadataType(**attrs)
        try:
            instance.full_clean()
        except DjangoValidationError as exception:
            raise ValidationError(exception)

        return attrs


class WritableDocumentTypeMetadataTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'required', 'url'
        )
        model = DocumentTypeMetadataType

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documenttypemetadatatype-detail', kwargs={
                'document_type_id': instance.document_type.pk,
                'metadata_type_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )


class DocumentMetadataSerializer(
    CreateOnlyFieldSerializerMixin, serializers.HyperlinkedModelSerializer
):
    metadata_type_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the metadata type to be added to the document.'
        ), source_model=MetadataType,
        source_permission=permission_document_metadata_add
    )
    document = DocumentSerializer(read_only=True)
    metadata_type = MetadataTypeSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        create_only_fields = ('metadata_type_id',)
        fields = (
            'document', 'id', 'metadata_type', 'metadata_type_id', 'url',
            'value'
        )
        model = DocumentMetadata
        read_only_fields = ('document', 'metadata_type',)

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documentmetadata-detail', kwargs={
                'document_id': instance.document.pk,
                'metadata_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def validate(self, attrs):
        if self.instance:
            self.instance.value = attrs['value']

            try:
                self.instance.full_clean()
            except DjangoValidationError as exception:
                raise ValidationError(exception)

            attrs['value'] = self.instance.value

            return attrs
        else:
            attrs['document'] = self.context['external_object']
            attrs['metadata_type'] = MetadataType.objects.get(
                pk=attrs.pop('metadata_type_id').pk
            )

            instance = DocumentMetadata(**attrs)
            try:
                instance.full_clean()
            except DjangoValidationError as exception:
                raise ValidationError(exception)

            attrs['value'] = instance.value

            return attrs
