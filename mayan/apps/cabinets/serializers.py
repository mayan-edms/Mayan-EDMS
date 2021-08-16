from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_recursive.fields import RecursiveField

from mayan.apps.documents.models import Document
from mayan.apps.rest_api.relations import FilteredPrimaryKeyRelatedField

from .models import Cabinet
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_remove_document
)


class CabinetSerializer(serializers.ModelSerializer):
    children = RecursiveField(
        help_text=_('List of children cabinets.'), many=True, read_only=True
    )
    documents_url = serializers.HyperlinkedIdentityField(
        help_text=_(
            'URL of the API endpoint showing the list documents inside this '
            'cabinet.'
        ), lookup_url_kwarg='cabinet_id',
        view_name='rest_api:cabinet-document-list'
    )
    full_path = serializers.SerializerMethodField(
        help_text=_(
            'The name of this cabinet level appended to the names of its '
            'ancestors.'
        ), read_only=True
    )
    parent_url = serializers.SerializerMethodField(read_only=True)

    # This is here because parent is optional in the model but the serializer
    # sets it as required.
    parent = serializers.PrimaryKeyRelatedField(
        allow_null=True, queryset=Cabinet.objects.all(), required=False
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'cabinet_id',
                'view_name': 'rest_api:cabinet-detail'
            },
        }
        fields = (
            'children', 'documents_url', 'full_path', 'id', 'label',
            'parent', 'parent_url', 'url'
        )
        model = Cabinet
        read_only_fields = (
            'children', 'documents_url', 'full_path', 'id',
            'parent_url', 'url'
        )

    def get_full_path(self, obj):
        return obj.get_full_path()

    def get_parent_url(self, obj):
        if obj.parent:
            return reverse(
                viewname='rest_api:cabinet-detail',
                kwargs={'cabinet_id': obj.parent.pk},
                format=self.context['format'],
                request=self.context.get('request')
            )
        else:
            return ''


class CabinetDocumentAddSerializer(serializers.Serializer):
    document = FilteredPrimaryKeyRelatedField(
        source_queryset=Document.valid,
        source_permission=permission_cabinet_add_document
    )


class CabinetDocumentRemoveSerializer(serializers.Serializer):
    document = FilteredPrimaryKeyRelatedField(
        source_queryset=Document.valid,
        source_permission=permission_cabinet_remove_document
    )
