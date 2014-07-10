from __future__ import absolute_import

from rest_framework import serializers

from .models import Document, DocumentVersion, DocumentPage


class DocumentPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentPage


class DocumentVersionSerializer(serializers.HyperlinkedModelSerializer):
    pages = DocumentPageSerializer(many=True, read_only=True)

    class Meta:
        model = DocumentVersion


class DocumentImageSerializer(serializers.Serializer):
    status = serializers.CharField()
    data = serializers.CharField()


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)
    image = serializers.HyperlinkedIdentityField(view_name='document-image')

    class Meta:
        model = Document
