from rest_framework import serializers

from .models import DocumentPageOCRContent, DocumentTypeSettings


class DocumentPageOCRContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentPageOCRContent


class DocumentTypeOCRSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('auto_ocr',)
        model = DocumentTypeSettings
