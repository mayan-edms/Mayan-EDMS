from rest_framework import serializers

from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from ..models.document_version_models import DocumentVersion
from ..models.document_version_page_models import DocumentVersionPage


class DocumentVersionSerializer(serializers.HyperlinkedModelSerializer):
    document_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:document-detail'
    )
    export_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_version_id',
            },
        ),
        view_name='rest_api:documentversion-export'
    )
    pages_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_version_id',
            },
        ),
        view_name='rest_api:documentversionpage-list'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_version_id',
            },
        ),
        view_name='rest_api:documentversion-detail'
    )

    class Meta:
        fields = (
            'comment', 'document_url', 'export_url', 'id', 'pages_url',
            'timestamp', 'url'
        )
        model = DocumentVersion


class DocumentVersionPageSerializer(serializers.HyperlinkedModelSerializer):
    document_version_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'document_version_id',
            }
        ),
        view_name='rest_api:documentversion-detail'
    )
    image_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'document_version_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_version_page_id',
            }
        ),
        view_name='rest_api:documentversionpage-image'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_version.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_version_id',
                'lookup_url_kwarg': 'document_version_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_version_page_id',
            }
        ),
        view_name='rest_api:documentversionpage-detail'
    )

    class Meta:
        fields = ('document_version_url', 'image_url', 'page_number', 'url')
        model = DocumentVersionPage
