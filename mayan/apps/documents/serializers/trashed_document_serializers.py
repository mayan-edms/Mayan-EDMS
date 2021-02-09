from rest_framework import serializers

from ..models.trashed_document_models import TrashedDocument

from .document_serializers import DocumentSerializer


class TrashedDocumentSerializer(DocumentSerializer):
    restore_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:trasheddocument-restore'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'document_id',
                'view_name': 'rest_api:trasheddocument-detail'
            }
        }
        fields = sorted(
            DocumentSerializer.Meta.fields + (
                'restore_url', 'trashed_date_time'
            )
        )
        model = TrashedDocument
