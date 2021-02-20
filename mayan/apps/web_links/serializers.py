from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.serializers.document_type_serializers import (
    DocumentTypeSerializer
)
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.rest_api.relations import FilteredPrimaryKeyRelatedField

from .models import ResolvedWebLink, WebLink


class WebLinkDocumentTypeAttachSerializer(serializers.Serializer):
    document_type = FilteredPrimaryKeyRelatedField(
        source_model=DocumentType,
        source_permission=permission_document_type_edit
    )


class WebLinkDocumentTypeRemoveSerializer(serializers.Serializer):
    document_type = FilteredPrimaryKeyRelatedField(
        source_model=DocumentType,
        source_permission=permission_document_type_edit
    )


class WebLinkSerializer(serializers.HyperlinkedModelSerializer):
    document_types = DocumentTypeSerializer(read_only=True, many=True)

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'web_link_id',
                'view_name': 'rest_api:web_link-detail'
            },
        }
        fields = (
            'document_types', 'enabled', 'id', 'label', 'template', 'url'
        )
        model = WebLink


class ResolvedWebLinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    navigation_url = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'navigation_url', 'url')
        model = ResolvedWebLink

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:resolved_web_link-detail',
            kwargs={
                'document_id': self.context['external_object'].pk,
                'resolved_web_link_id': instance.pk
            }, request=self.context['request'],
            format=self.context['format']
        )

    def get_navigation_url(self, instance):
        return reverse(
            viewname='rest_api:resolved_web_link-navigate',
            kwargs={
                'document_id': self.context['external_object'].pk,
                'resolved_web_link_id': instance.pk
            }, request=self.context['request'],
            format=self.context['format']
        )
