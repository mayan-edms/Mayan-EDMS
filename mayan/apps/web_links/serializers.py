from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.serializers import DocumentTypeSerializer
from mayan.apps.documents.permissions import permission_document_type_edit

from .models import ResolvedWebLink, WebLink


class WebLinkSerializer(serializers.HyperlinkedModelSerializer):
    document_types = DocumentTypeSerializer(read_only=True, many=True)

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'pk',
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
                'pk': self.context['document'].pk,
                'resolved_web_link_pk': instance.pk
            }, request=self.context['request'],
            format=self.context['format']
        )

    def get_navigation_url(self, instance):
        return reverse(
            viewname='rest_api:resolved_web_link-navigate',
            kwargs={
                'pk': self.context['document'].pk,
                'resolved_web_link_pk': instance.pk
            }, request=self.context['request'],
            format=self.context['format']
        )


class WritableWebLinkSerializer(serializers.ModelSerializer):
    document_types_pk_list = serializers.CharField(
        help_text=_(
            'Comma separated list of document type primary keys to which '
            'this web link will be attached.'
        ), required=False
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:web_link-detail'},
        }
        fields = (
            'document_types_pk_list', 'enabled', 'label', 'id', 'template',
            'url'
        )
        model = WebLink

    def validate(self, attrs):
        document_types_pk_list = attrs.pop('document_types_pk_list', None)

        if document_types_pk_list:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission_document_type_edit,
                queryset=DocumentType.objects.filter(
                    pk__in=document_types_pk_list.split(',')
                ), user=self.context['request'].user
            )

            attrs['document_types'] = queryset
        else:
            attrs['document_types'] = ()
        return attrs
