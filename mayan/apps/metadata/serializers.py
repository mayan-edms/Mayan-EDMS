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
from .permissions import permission_metadata_add

'''
class DocumentMetadataSerializer(serializers.HyperlinkedModelSerializer):
    document = DocumentSerializer(read_only=True)
    metadata_type = MetadataTypeSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        fields = ('document', 'id', 'metadata_type', 'url', 'value')
        model = DocumentMetadata
        read_only_fields = ('document', 'metadata_type',)

    def get_url(self, instance):
        return reverse(
            'rest_api:documentmetadata-detail', args=(
                instance.document.pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    def validate(self, attrs):
        self.instance.value = attrs['value']

        try:
            self.instance.full_clean()
        except DjangoValidationError as exception:
            raise ValidationError(exception)

        return attrs


class NewDocumentMetadataSerializer(serializers.ModelSerializer):
    metadata_type_pk = serializers.IntegerField(
        help_text=_(
            'Primary key of the metadata type to be added to the document.'
        ),
        write_only=True
    )
    url = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'metadata_type_pk', 'url', 'value')
        model = DocumentMetadata

    def create(self, validated_data):
        queryset = AccessControlList.objects.restrict_queryset(
            queryset=MetadataType.objects.all(),
            permission=permission_metadata_add,
            user=self.context['request'].user
        )
        get_object_or_404(
            klass=queryset, pk=validated_data['metadata_type'].pk
        )

        return super(NewDocumentMetadataSerializer, self).create(
            validated_data=validated_data
        )

    def get_url(self, instance):
        return reverse(
            'rest_api:documentmetadata-detail', args=(
                instance.document.pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    def validate(self, attrs):
        attrs['document'] = self.context['document']
        attrs['metadata_type'] = MetadataType.objects.get(
            pk=attrs.pop('metadata_type_pk')
        )

        instance = DocumentMetadata(**attrs)
        try:
            instance.full_clean()
        except DjangoValidationError as exception:
            raise ValidationError(exception)

        return attrs
'''


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


class MetadataTypeDocumentTypeRelationSerializer(
    CreateOnlyFieldSerializerMixin, ExternalObjectSerializerMixin,
    serializers.HyperlinkedModelSerializer
):
    document_type = DocumentTypeSerializer(read_only=True)
    document_type_id = serializers.IntegerField(
        help_text=_(
            'Primary keys of the document type that will be added or removed.'
        ), label=_('Document Type ID'), write_only=True
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
        fields = ('document_type', 'document_type_id', 'id', 'required', 'url')
        model = DocumentTypeMetadataType

    def create(self, validated_data):
        validated_data['document_type'] = self.get_external_object()
        validated_data['metadata_type'] = self.context['external_object']

        return super(MetadataTypeDocumentTypeRelationSerializer, self).create(
            validated_data=validated_data
        )
