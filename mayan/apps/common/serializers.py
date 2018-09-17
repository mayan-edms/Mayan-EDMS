from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('app_label', 'id', 'model')
        model = ContentType


class TemplateSerializer(serializers.Serializer):
    hex_hash = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    html = serializers.CharField(read_only=True)
