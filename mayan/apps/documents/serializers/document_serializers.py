from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.rest_api.serializer_mixins import CreateOnlyFieldSerializerMixin
from mayan.apps.storage.models import SharedUploadedFile

from ..models.document_models import Document
from ..models.document_type_models import DocumentType

from ..tasks import task_document_file_upload

from .document_file_serializers import DocumentFileSerializer
from .document_type_serializers import DocumentTypeSerializer
from .document_version_serializers import DocumentVersionSerializer


class DocumentSerializer(
    CreateOnlyFieldSerializerMixin, serializers.HyperlinkedModelSerializer
):
    document_type = DocumentTypeSerializer(read_only=True)
    document_type_id = serializers.IntegerField(
        help_text=_('Document type ID for the new document.'), write_only=True
    )
    document_change_type_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:document-change-type'
    )
    file_latest = DocumentFileSerializer(many=False, read_only=True)
    file_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:documentfile-list'
    )
    version_active = DocumentVersionSerializer(many=False, read_only=True)
    version_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='document_id',
        view_name='rest_api:documentversion-list'
    )

    class Meta:
        create_only_fields = ('document_type_id',)
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'document_id',
                'view_name': 'rest_api:document-detail'
            },
        }
        fields = (
            'datetime_created', 'description', 'document_change_type_url',
            'document_type', 'document_type_id', 'file_list_url', 'id', 'label',
            'language', 'file_latest', 'url', 'uuid', 'version_active',
            'version_list_url'
        )
        model = Document
        read_only_fields = ('document_type',)


class DocumentChangeTypeSerializer(serializers.ModelSerializer):
    document_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(), write_only=True
    )

    class Meta:
        fields = ('document_type_id',)
        model = Document


class DocumentUploadSerializer(DocumentSerializer):
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

    class Meta(DocumentSerializer.Meta):
        create_only_fields = ('document_type_id', 'file')
        fields = (
            'datetime_created', 'description', 'document_change_type_url',
            'document_type', 'document_type_id', 'file', 'file_list_url',
            'id', 'label', 'language', 'file_latest', 'pk', 'url', 'uuid',
            'version_active', 'version_list_url'
        )
