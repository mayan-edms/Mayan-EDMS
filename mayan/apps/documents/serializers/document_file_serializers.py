from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField
from mayan.apps.rest_api.serializer_mixins import CreateOnlyFieldSerializerMixin

from ..literals import DOCUMENT_FILE_ACTION_PAGE_CHOICES
from ..models.document_file_models import DocumentFile
from ..models.document_file_page_models import DocumentFilePage


class DocumentFileSerializer(
    CreateOnlyFieldSerializerMixin, serializers.HyperlinkedModelSerializer
):
    action = serializers.ChoiceField(
        choices=DOCUMENT_FILE_ACTION_PAGE_CHOICES
    )
    document_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:document-detail'
    )
    download_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_id',
            },
        ),
        view_name='rest_api:documentfile-download'
    )
    file_new = serializers.FileField(
        help_text=_('Binary content for the new file.'),
        use_url=False
    )
    page_list_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_id',
            },
        ),
        view_name='rest_api:documentfilepage-list'
    )
    size = serializers.SerializerMethodField()
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_id',
            },
        ),
        view_name='rest_api:documentfile-detail'
    )

    class Meta:
        create_only_fields = ('action', 'file_new',)
        extra_kwargs = {
            'file': {'use_url': False},
        }
        fields = (
            'action', 'checksum', 'comment', 'document_url', 'download_url', 'encoding',
            'file', 'filename', 'file_new', 'id', 'mimetype', 'page_list_url',
            'size', 'timestamp', 'url'
        )
        model = DocumentFile
        read_only_fields = ('document', 'file', 'size')

    def get_size(self, instance):
        return instance.size


class DocumentFilePageSerializer(serializers.HyperlinkedModelSerializer):
    document_file_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id',
            }
        ),
        view_name='rest_api:documentfile-detail'
    )
    image_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_page_id',
            }
        ),
        view_name='rest_api:documentfilepage-image'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_page_id',
            }
        ),
        view_name='rest_api:documentfilepage-detail'
    )

    class Meta:
        fields = (
            'document_file_url', 'id', 'image_url', 'page_number', 'url'
        )
        model = DocumentFilePage
