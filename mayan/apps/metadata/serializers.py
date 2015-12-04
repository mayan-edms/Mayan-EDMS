from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import DocumentMetadata, MetadataType, DocumentTypeMetadataType


class MetadataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'label', 'default', 'lookup')
        model = MetadataType


class DocumentMetadataSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('document', 'id', 'metadata_type', 'value',)
        model = DocumentMetadata


class DocumentTypeMetadataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('metadata_type', )
        model = DocumentTypeMetadataType


class DocumentNewMetadataSerializer(serializers.Serializer):
    metadata_type = serializers.IntegerField(
        help_text=_('Primary key of the metadata type to be added.')
    )
    value = serializers.CharField(
        max_length=255,
        help_text=_('Value of the corresponding metadata type instance.')
    )


class DocumentTypeNewMetadataTypeSerializer(serializers.Serializer):
    metadata_type = serializers.IntegerField(
        help_text=_('Primary key of the metadata type to be added.')
    )
