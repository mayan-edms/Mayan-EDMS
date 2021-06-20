from rest_framework import serializers

from mayan.apps.user_management.serializers import UserSerializer

from ..models.recently_accessed_document_models import RecentlyAccessedDocument

from .document_serializers import DocumentSerializer


class RecentlyAccessedDocumentSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        fields = ('document', 'id', 'datetime_accessed', 'user')
        model = RecentlyAccessedDocument
        read_only_fields = ('document', 'id', 'datetime_accessed', 'user')
