from __future__ import unicode_literals

from rest_framework import serializers


class APIResourceSerializer(serializers.Serializer):
    description = serializers.CharField()
    label = serializers.CharField()
    name = serializers.CharField()
