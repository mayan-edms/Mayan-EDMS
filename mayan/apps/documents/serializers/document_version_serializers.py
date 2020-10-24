from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models.document_version_models import DocumentVersion
from ..models.document_version_page_models import DocumentVersionPage


class DocumentVersionSerializer(serializers.HyperlinkedModelSerializer):
    document_url = serializers.SerializerMethodField()
    export_url = serializers.SerializerMethodField()
    pages_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'document': {
                'lookup_url_kwarg': 'document_id',
                'view_name': 'rest_api:document-detail'
            },
        }
        fields = (
            'comment', 'document_url', 'export_url', 'id', 'pages_url',
            'timestamp', 'url'
        )
        model = DocumentVersion
        read_only_fields = ('document',)

    def get_document_url(self, instance):
        return reverse(
            viewname='rest_api:document-detail', kwargs={
                'document_id': instance.document_id,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_export_url(self, instance):
        return reverse(
            viewname='rest_api:documentversion-export', kwargs={
                'document_id': instance.document_id,
                'document_version_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_pages_url(self, instance):
        return reverse(
            viewname='rest_api:documentversionpage-list', kwargs={
                'document_id': instance.document_id,
                'document_version_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:documentversion-detail', kwargs={
                'document_id': instance.document_id,
                'document_version_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
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
