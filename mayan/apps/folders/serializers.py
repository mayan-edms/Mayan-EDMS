from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from documents.serializers import DocumentSerializer

from .models import Folder


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='rest_api:folder-document-list'
    )
    documents_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:folder-detail'},
        }
        fields = (
            'datetime_created', 'documents', 'documents_count', 'id', 'label',
            'url'
        )
        model = Folder

    def get_documents_count(self, obj):
        return obj.documents.count()


class NewFolderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('label', 'id')
        model = Folder


class FolderDocumentSerializer(DocumentSerializer):
    remove = serializers.SerializerMethodField()

    def get_remove(self, instance):
        return reverse(
            'rest_api:folder-document', args=(
                self.context['folder'].pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ('remove',)
        read_only_fields = DocumentSerializer.Meta.fields


class NewFolderDocumentSerializer(serializers.Serializer):
    document = serializers.IntegerField(
        help_text=_('Primary key of the document to be added.')
    )

    def create(self, validated_data):
        try:
            document = Document.objects.get(pk=validated_data['document'])
            validated_data['folder'].documents.add(document)
        except Exception as exception:
            raise ValidationError(exception)

        return {'document': document.pk}
