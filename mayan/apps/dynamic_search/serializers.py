from __future__ import unicode_literals

from rest_framework import serializers

from .classes import SearchModel


class SearchModelSerializer(serializers.Serializer):
    app_label = serializers.CharField(read_only=True)
    model_name = serializers.CharField(read_only=True)
    pk = serializers.CharField(read_only=True)
