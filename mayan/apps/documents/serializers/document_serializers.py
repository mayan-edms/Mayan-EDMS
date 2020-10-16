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

from .document_file_serializers import DocumentFileSerializer
from .document_type_serializers import DocumentTypeSerializer
from .document_version_serializers import DocumentVersionSerializer


class DocumentCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    def create(self, validated_data):
        file = validated_data.pop('file')
        validated_data['label'] = validated_data.get('label', str(file))
        user = validated_data['_instance_extra_data']['_event_actor']

        instance = super().create(validated_data=validated_data)

        shared_uploaded_file = SharedUploadedFile.objects.create(file=file)

        task_document_file_upload.apply_async(
            kwargs={
                'document_id': instance.pk,
                'shared_uploaded_file_id': shared_uploaded_file.pk,
                'user_id': user.pk
            }
        )

        return instance

    class Meta:
        fields = (
            'description', 'document_type', 'id', 'file', 'label', 'language',
        )
        model = Document


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)
    document_type_change_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:document-type-change'
    )
    latest_file = DocumentFileSerializer(many=False, read_only=True)
    file_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:documentfile-list'
    )
    latest_version = DocumentVersionSerializer(many=False, read_only=True)
    version_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:documentversion-list'
    )

    class Meta:
        extra_kwargs = {
            'document_type': {
                'lookup_url_kwarg': 'document_type_id',
                'view_name': 'rest_api:documenttype-detail'
            },
            'url': {
                'lookup_url_kwarg': 'document_id',
                'view_name': 'rest_api:document-detail'
            },
        }
        fields = (
            'date_added', 'description', 'document_type',
            'document_type_change_url', 'file_list_url', 'id', 'label',
            'language', 'latest_file', 'latest_version', 'pk', 'url', 'uuid',
            'version_list_url'
        )
        model = Document
        read_only_fields = ('document_type',)


class DocumentTypeChangeSerializer(serializers.ModelSerializer):
    new_document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), write_only=True
    )

    class Meta:
        fields = ('new_document_type',)
        model = Document


class DocumentWritableSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer(read_only=True)
    latest_file = DocumentFileSerializer(many=False, read_only=True)
    files = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:documentfile-list'
    )
    url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:document-detail'
    )

    class Meta:
        fields = (
            'date_added', 'description', 'document_type', 'id', 'label',
            'language', 'latest_file', 'url', 'uuid', 'files',
        )
        model = Document
        read_only_fields = ('document_type',)


class RecentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('document', 'datetime_accessed')
        model = RecentDocument


class TrashedDocumentSerializer(serializers.HyperlinkedModelSerializer):
    document_type_label = serializers.SerializerMethodField()
    restore = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
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
