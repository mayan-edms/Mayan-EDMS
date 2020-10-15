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


class DocumentTypeFilenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypeFilename
        fields = ('filename',)


class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):
    documents_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_type_id',
        view_name='rest_api:documenttype-document-list'
    )
    documents_count = serializers.SerializerMethodField()
    filenames = DocumentTypeFilenameSerializer(many=True, read_only=True)

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'document_type_id',
                'view_name': 'rest_api:documenttype-detail'
            },
        }
        fields = (
            'delete_time_period', 'delete_time_unit', 'documents_url',
            'documents_count', 'id', 'label', 'filenames', 'trash_time_period',
            'trash_time_unit', 'url'
        )
        model = DocumentType

    def get_documents_count(self, obj):
        return obj.documents.count()


class DocumentTypeWritableSerializer(serializers.ModelSerializer):
    documents_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_type_id',
        view_name='rest_api:documenttype-document-list'
    )
    documents_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'document_type_id',
                'view_name': 'rest_api:documenttype-detail'
            },
        }
        fields = (
            'delete_time_period', 'delete_time_unit', 'documents_url',
            'documents_count', 'id', 'label', 'trash_time_period',
            'trash_time_unit', 'url'
        )
        model = DocumentType

    def get_documents_count(self, obj):
        return obj.documents.count()
