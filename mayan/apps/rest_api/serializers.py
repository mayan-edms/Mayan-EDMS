from __future__ import unicode_literals

from rest_framework import serializers


class EndpointSerializer(serializers.Serializer):
    label = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
