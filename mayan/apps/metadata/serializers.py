from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import DocumentMetadata, MetadataType


class MetadataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'title', 'default', 'lookup')
        model = MetadataType


class DocumentMetadataNestedSerializer(serializers.ModelSerializer):
    metadata_type = MetadataTypeSerializer()

    class Meta:
        fields = ('id', 'metadata_type', 'value')
        model = DocumentMetadata


class DocumentMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'metadata_type', 'value')
        model = DocumentMetadata


class DocumentTypeNewMetadataTypeSerializer(serializers.Serializer):
    metadata_type_pk = serializers.IntegerField(help_text=_('Primary key of the metadata type to be added.'))
