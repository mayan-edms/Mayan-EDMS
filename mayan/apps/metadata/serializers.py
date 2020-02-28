from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.serializers import (
    DocumentSerializer, DocumentTypeSerializer
)
from mayan.apps.rest_api.mixins import (
    CreateOnlyFieldSerializerMixin, ExternalObjectSerializerMixin
)
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from .models import DocumentMetadata, DocumentTypeMetadataType, MetadataType
from .permissions import permission_metadata_add, permission_metadata_type_edit


class MetadataTypeSerializer(serializers.HyperlinkedModelSerializer):
    document_type_relation_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='metadata_type_id',
        view_name='rest_api:metadata_type-document_type_relation-list'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'metadata_type_id',
                'view_name': 'rest_api:metadata_type-detail'
            },
        }
        fields = (
            'default', 'document_type_relation_list_url', 'id', 'label',
            'lookup', 'name', 'parser', 'url', 'validation'
        )
        model = MetadataType


class DocumentMetadataSerializer(
    CreateOnlyFieldSerializerMixin, ExternalObjectSerializerMixin,
    serializers.HyperlinkedModelSerializer
):
    document = DocumentSerializer(read_only=True)
    metadata_type = MetadataTypeSerializer(read_only=True)
    metadata_type_id = serializers.IntegerField(
        help_text=_(
            'Primary key of the metadata type that will be added or removed.'
        ), label=_('Metadata type ID'), write_only=True
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_metadata_id',
            }
        ),
        view_name='rest_api:document_metadata-detail'
    )

    class Meta:
        create_only_fields = ('metadata_type_id',)
        external_object_model = MetadataType
        external_object_permission = permission_metadata_add
        external_object_pk_field = 'metadata_type_id'
        fields = (
            'document', 'id', 'metadata_type', 'metadata_type_id', 'url',
            'value'
        )
        model = DocumentMetadata

    def create(self, validated_data):
        validated_data['document'] = self.context['external_object']
        validated_data['metadata_type'] = self.get_external_object()

        return super(DocumentMetadataSerializer, self).create(
            validated_data=validated_data
        )

    def validate(self, attrs):
        if self.instance:
            self.instance.value = attrs['value']
            self.instance.full_clean()

            return attrs
        else:
            attrs['document'] = self.context['external_object']
            attrs['metadata_type'] = self.get_external_object()

            instance = DocumentMetadata(**attrs)
            instance.full_clean()

            return attrs


class DocumentTypeMetadataTypeRelationSerializer(
    CreateOnlyFieldSerializerMixin, ExternalObjectSerializerMixin,
    serializers.HyperlinkedModelSerializer
):
    metadata_type = MetadataTypeSerializer(read_only=True)
    metadata_type_id = serializers.IntegerField(
        help_text=_(
            'Primary key of the metadata type that will be added or removed.'
        ), label=_('Metadata type ID'), write_only=True
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_type_id',
                'lookup_url_kwarg': 'document_type_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_type_metadata_type_relation_id',
            }
        ),
        view_name='rest_api:document_type-metadata_type_relation-detail'
    )

    class Meta:
        create_only_fields = ('metadata_type_id',)
        external_object_model = MetadataType
        external_object_permission = permission_metadata_type_edit
        external_object_pk_field = 'metadata_type_id'
        fields = (
            'metadata_type', 'metadata_type_id', 'id', 'required', 'url'
        )
        model = DocumentTypeMetadataType

    def create(self, validated_data):
        validated_data['metadata_type'] = self.get_external_object()
        validated_data['document_type'] = self.context['external_object']

        return super(DocumentTypeMetadataTypeRelationSerializer, self).create(
            validated_data=validated_data
        )


class MetadataTypeDocumentTypeRelationSerializer(
    CreateOnlyFieldSerializerMixin, ExternalObjectSerializerMixin,
    serializers.HyperlinkedModelSerializer
):
    document_type = DocumentTypeSerializer(read_only=True)
    document_type_id = serializers.IntegerField(
        help_text=_(
            'Primary key of the document type that will be added or removed.'
        ), label=_('Document type ID'), write_only=True
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'metadata_type_id',
                'lookup_url_kwarg': 'metadata_type_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'metadata_type_document_type_relation_id',
            }
        ),
        view_name='rest_api:metadata_type-document_type_relation-detail'
    )

    class Meta:
        create_only_fields = ('document_type_id',)
        external_object_model = DocumentType
        external_object_permission = permission_document_type_edit
        external_object_pk_field = 'document_type_id'
        fields = (
            'document_type', 'document_type_id', 'id', 'required', 'url'
        )
        model = DocumentTypeMetadataType

    def create(self, validated_data):
        validated_data['document_type'] = self.get_external_object()
        validated_data['metadata_type'] = self.context['external_object']

        return super(MetadataTypeDocumentTypeRelationSerializer, self).create(
            validated_data=validated_data
        )
