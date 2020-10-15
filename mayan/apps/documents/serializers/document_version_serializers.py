from django.utils.encoding import force_text

from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.storage.models import SharedUploadedFile

from ..models.document_models import Document
from ..models.document_file_models import DocumentFile
from ..models.document_file_page_models import DocumentFilePage
from ..models.document_type_models import DocumentType, DocumentTypeFilename
from ..models.document_version_models import DocumentVersion
from ..models.document_version_page_models import DocumentVersionPage
from ..models.misc_models import RecentDocument

from ..settings import setting_language
from ..tasks import task_document_file_upload


class DocumentVersionSerializer(serializers.HyperlinkedModelSerializer):
    document_url = serializers.SerializerMethodField()
    export_url = serializers.SerializerMethodField()
    pages_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'document': {'view_name': 'rest_api:document-detail'},
        }
        fields = (
            'checksum', 'comment', 'document_url', 'export_url',
            'pages_url', 'timestamp', 'url'
        )
        model = DocumentVersion
        read_only_fields = ('document',)

    def get_document_url(self, instance):
        return reverse(
            viewname='rest_api:document-detail', args=(
                instance.document_id,
            ), request=self.context['request'], format=self.context['format']
        )

    def get_export_url(self, instance):
        return reverse(
            viewname='rest_api:documentversion-export', args=(
                instance.document_id, instance.pk,
            ), request=self.context['request'], format=self.context['format']
        )

    def get_pages_url(self, instance):
        return reverse(
            viewname='rest_api:documentversionpage-list', args=(
                instance.document_id, instance.pk,
            ), request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documentversion-detail', args=(
                instance.document_id, instance.pk,
            ), request=self.context['request'], format=self.context['format']
        )


class DocumentVersionPageSerializer(serializers.HyperlinkedModelSerializer):
    document_version_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        fields = ('document_version_url', 'image_url', 'page_number', 'url')
        model = DocumentVersionPage

    def get_document_version_url(self, instance):
        return reverse(
            viewname='rest_api:documentversion-detail', kwargs={
                'document_id': instance.document_version.document_id,
                'document_version_id': instance.document_version_id
            }, request=self.context['request'], format=self.context['format']
        )

    def get_image_url(self, instance):
        return reverse(
            viewname='rest_api:documentversionpage-image', kwargs={
                'document_id': instance.document_version.document_id,
                'document_version_id': instance.document_version_id,
                'document_version_page_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documentversionpage-detail', kwargs={
                'document_id': instance.document_version.document_id,
                'document_version_id': instance.document_version_id,
                'document_version_page_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )


class RecentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('document', 'datetime_accessed')
        model = RecentDocument


class TrashedDocumentSerializer(serializers.HyperlinkedModelSerializer):
    document_type_label = serializers.SerializerMethodField()
    restore = serializers.HyperlinkedIdentityField(
        view_name='rest_api:trasheddocument-restore'
    )

    class Meta:
        extra_kwargs = {
            'document_type': {
                'lookup_url_kwarg': 'document_type_id',
                'view_name': 'rest_api:documenttype-detail'
            },
            'url': {
                'lookup_url_kwarg': 'document_id',
                'view_name': 'rest_api:trasheddocument-detail'
            }
        }
        fields = (
            'date_added', 'deleted_date_time', 'description', 'document_type',
            'document_type_label', 'id', 'label', 'language', 'restore',
            'url', 'uuid',
        )
        model = Document
        read_only_fields = (
            'deleted_date_time', 'description', 'document_type', 'label',
            'language'
        )

    def get_document_type_label(self, instance):
        return instance.document_type.label
