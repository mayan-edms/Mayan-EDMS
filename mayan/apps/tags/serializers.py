from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.documents.models import Document
from mayan.apps.rest_api.mixins import ExternalObjectListSerializerMixin

from .models import Tag
from .permissions import permission_tag_attach, permission_tag_remove


class DocumentTagAttachRemoveSerializer(
    ExternalObjectListSerializerMixin, serializers.Serializer
):
    tag_id_list = serializers.CharField(
        label=_('Tag ID list'), help_text=_(
            'Comma separated list of tag primary keys to be attached or '
            'removed.'
        ), required=False, write_only=True
    )

    class Meta:
        external_object_list_model = Tag
        external_object_list_pk_list_field = 'tag_id_list'

    def tags_attach(self, instance):
        instance.tags_attach(
            queryset=self.get_external_object_list(
                permission=permission_tag_attach
            ), _user=self.context['request'].user
        )

    def tags_remove(self, instance):
        instance.tags_remove(
            queryset=self.get_external_object_list(
                permission=permission_tag_remove
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
    ExternalObjectListSerializerMixin, serializers.Serializer
):
    document_id_list = serializers.CharField(
        label=_('Document ID list'), help_text=_(
            'Comma separated list of document primary keys to which this '
            'tag will be attached or removed.'
        ), required=False, write_only=True
    )

    class Meta:
        external_object_list_model = Document
        external_object_list_pk_list_field = 'document_id_list'

    def documents_attach(self, instance):
        instance.documents_attach(
            queryset=self.get_external_object_list(
                permission=permission_tag_attach
            ),
            _user=self.context['request'].user
        )

    def documents_remove(self, instance):
        instance.documents_remove(
            queryset=self.get_external_object_list(
                permission=permission_tag_remove
            ), _user=self.context['request'].user
        )
