from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'content_type_id',
                'view_name': 'rest_api:content_type-detail'
            }
        }
        fields = ('app_label', 'id', 'model', 'url')
        model = ContentType


class TemplateSerializer(serializers.Serializer):
    hex_hash = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    html = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        lookup_field='name', lookup_url_kwarg='template_name',
        view_name='rest_api:template-detail'
    )
