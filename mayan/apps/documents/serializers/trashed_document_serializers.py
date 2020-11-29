from rest_framework import serializers

from ..models.trashed_document_models import TrashedDocument

from .document_type_serializers import DocumentTypeSerializer


class TrashedDocumentSerializer(serializers.HyperlinkedModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)
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
        fields = (
            'datetime_created', 'description', 'document_type',
            'id', 'label', 'language', 'restore_url',
            'trashed_date_time', 'url', 'uuid'
        )
        model = TrashedDocument
