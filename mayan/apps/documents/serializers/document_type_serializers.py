from rest_framework import serializers

from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from ..models.document_type_models import DocumentType, DocumentTypeFilename


class DocumentTypeQuickLabelSerializer(serializers.ModelSerializer):
    document_type_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_type_id',
        view_name='rest_api:documenttype-detail'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_type_id',
                'lookup_url_kwarg': 'document_type_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_type_quick_label_id',
            },
        ),
        view_name='rest_api:documenttype-quicklabel-detail'
    )

    class Meta:
        model = DocumentTypeFilename
        fields = ('document_type_url', 'enabled', 'filename', 'id', 'url')


class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):
    documents_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_type_id',
        view_name='rest_api:documenttype-document-list'
    )
    quick_label_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_type_id',
        view_name='rest_api:documenttype-quicklabel-list'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'document_type_id',
                'view_name': 'rest_api:documenttype-detail'
            },
        }
        fields = (
            'delete_time_period', 'delete_time_unit', 'documents_url',
            'id', 'label', 'quick_label_list_url', 'trash_time_period',
            'trash_time_unit', 'url'
        )
        model = DocumentType
