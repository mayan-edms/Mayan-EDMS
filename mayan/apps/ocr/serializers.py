from rest_framework import serializers

from .models import DocumentPageOCRContent


class DocumentPageOCRContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content',)
        model = DocumentPageOCRContent
