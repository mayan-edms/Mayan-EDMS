from __future__ import unicode_literals

from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    label = serializers.CharField()
    name = serializers.CharField()
