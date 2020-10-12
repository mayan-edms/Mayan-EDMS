from rest_framework import serializers

from .models import DocumentFilePageContent, DocumentTypeSettings


class DocumentFilePageContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentFilePageContent


class DocumentTypeParsingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('auto_parsing',)
        model = DocumentTypeSettings
