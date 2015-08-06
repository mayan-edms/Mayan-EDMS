from __future__ import unicode_literals

from rest_framework import serializers


class APIVersionSerializer(serializers.Serializer):
    url = serializers.URLField()
    version_string = serializers.CharField()


class APIAppSerializer(serializers.Serializer):
    app_name = serializers.CharField()
    url = serializers.URLField()
    version_string = serializers.CharField()
