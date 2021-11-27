from mayan.apps.rest_api import serializers

from .models import DocumentVersionPageOCRContent, DocumentTypeOCRSettings


class DocumentVersionPageOCRContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentVersionPageOCRContent
        read_only_fields = ()


class DocumentTypeOCRSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('auto_ocr',)
        model = DocumentTypeOCRSettings
        read_only_fields = ()
