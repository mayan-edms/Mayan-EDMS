from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serializers import ContentTypeSerializer
from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from ..models.document_version_models import DocumentVersion
from ..models.document_version_page_models import DocumentVersionPage


class DocumentVersionPageSerializer(serializers.HyperlinkedModelSerializer):
    content_type = ContentTypeSerializer(read_only=True)
    content_type_id = serializers.IntegerField(
        help_text=_('Content type ID of the source object for the page.'),
        write_only=True
    )
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
        fields = (
            'content_type', 'content_type_id', 'document_version_id',
            'document_version_url', 'id', 'image_url', 'object_id',
            'page_number', 'url'
        )
        model = DocumentVersionPage
        read_only_fields = (
            'content_type', 'document_version_id', 'document_version_url',
            'id', 'image_url', 'url'
        )


class DocumentVersionSerializer(serializers.HyperlinkedModelSerializer):
    document_url = serializers.HyperlinkedIdentityField(
        lookup_field='document_id',
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
    page_list_url = MultiKwargHyperlinkedIdentityField(
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
    pages_first = DocumentVersionPageSerializer(many=False, read_only=True)
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
            'active', 'comment', 'document_id', 'document_url', 'export_url',
            'id', 'page_list_url', 'pages_first', 'timestamp', 'url'
        )
        model = DocumentVersion
        read_only_fields = (
            'document_id', 'document_url', 'export_url', 'id',
            'page_list_url', 'pages_first', 'timestamp', 'url'
        )
