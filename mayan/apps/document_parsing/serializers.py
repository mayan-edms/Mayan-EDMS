from mayan.apps.rest_api import serializers

from .models import DocumentFilePageContent, DocumentTypeSettings


class DocumentFilePageContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentFilePageContent
        read_only_fields = ('content',)


class DocumentTypeParsingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('auto_parsing',)
        model = DocumentTypeSettings
        read_only_fields = ()
