from rest_framework import serializers

from mayan.apps.documents.serializers.document_serializers import DocumentSerializer

from .models import DuplicateTargetDocument


class DuplicateTargetDocumentSerializer(DocumentSerializer):
    backend = serializers.CharField(read_only=True)

    class Meta(DocumentSerializer.Meta):
        fields = sorted(
            DocumentSerializer.Meta.fields + (
                'backend',
            )
        )
        model = DuplicateTargetDocument
