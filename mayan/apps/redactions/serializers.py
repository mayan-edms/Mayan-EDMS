from rest_framework import serializers


class DocumentVersionOCRSerializer(serializers.Serializer):
    document_version_id = serializers.IntegerField()
