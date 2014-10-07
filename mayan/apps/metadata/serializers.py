from __future__ import absolute_import

from rest_framework import serializers

from .models import DocumentMetadata, MetadataType


class MetadataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'title', 'default', 'lookup')
        model = MetadataType


class DocumentMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'document', 'metadata_type', 'value')
        model = DocumentMetadata
