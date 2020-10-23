from rest_framework import serializers

from .models import DocumentPageContent, DocumentTypeSettings


class DocumentPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentPageContent


class DocumentTypeParsingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('auto_parsing',)
        model = DocumentTypeSettings
