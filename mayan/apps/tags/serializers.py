from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.documents.models.document_models import Document
from mayan.apps.rest_api.mixins import ExternalObjectSerializerMixin

from .models import Tag
from .permissions import permission_tag_attach, permission_tag_remove


class DocumentTagAttachRemoveSerializer(
    ExternalObjectSerializerMixin, serializers.Serializer
):
    tag_id = serializers.IntegerField(
        label=_('Tag ID list'), help_text=_(
            'Primary key of the tag to attach or remove the selected '
            'document.'
        ), required=False, write_only=True
    )

    class Meta:
        external_object_model = Tag
        external_object_pk_field = 'tag_id'

    def tag_attach(self, instance):
        instance.tags_attach(
            queryset=self.get_external_object(
                as_queryset=True, permission=permission_tag_attach
            ), _user=self.context['request'].user
        )

    def tag_remove(self, instance):
        instance.tags_remove(
            queryset=self.get_external_object(
                as_queryset=True, permission=permission_tag_remove
            ), _user=self.context['request'].user
        )


class TagSerializer(serializers.HyperlinkedModelSerializer):
    document_attach_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='tag_id', view_name='rest_api:tag-document-attach'
    )

    document_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='tag_id', view_name='rest_api:tag-document-list'
    )

    document_remove_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='tag_id', view_name='rest_api:tag-document-remove'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'tag_id',
                'view_name': 'rest_api:tag-detail'
            },
        }
        fields = (
            'color', 'document_attach_url', 'document_list_url',
            'document_remove_url', 'label', 'id', 'url'
        )
        model = Tag


class TagDocumentAttachRemoveSerializer(
    ExternalObjectSerializerMixin, serializers.Serializer
):
    document_id = serializers.IntegerField(
        label=_('Document ID'),
        help_text=_(
            'Primary key of the document to attach or remove the selected '
            'tag.'
        ), required=True, write_only=True
    )

    class Meta:
        external_object_model = Document
        external_object_pk_field = 'document_id'

    def document_attach(self, instance):
        instance.documents_attach(
            queryset=self.get_external_object(
                as_queryset=True, permission=permission_tag_attach
            ), _user=self.context['request'].user
        )

    def document_remove(self, instance):
        instance.documents_remove(
            queryset=self.get_external_object(
                as_queryset=True, permission=permission_tag_remove
            ), _user=self.context['request'].user
        )
