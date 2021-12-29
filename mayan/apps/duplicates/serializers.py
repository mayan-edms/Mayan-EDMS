from mayan.apps.documents.serializers.document_serializers import DocumentSerializer
from mayan.apps.rest_api import serializers

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
