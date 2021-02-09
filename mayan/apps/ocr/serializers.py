from rest_framework import serializers

from .models import DocumentVersionPageOCRContent, DocumentTypeOCRSettings


class DocumentVersionPageOCRContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentVersionPageOCRContent


class DocumentTypeOCRSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('auto_ocr',)
        model = DocumentTypeOCRSettings
