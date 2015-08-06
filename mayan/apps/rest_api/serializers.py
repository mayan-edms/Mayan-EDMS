from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.reverse import reverse


class APIVersionSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    version_string = serializers.CharField()

    def get_url(self, instance):
        return reverse(
            'rest_api:api-version-1', format=self.context['format'],
            request=self.context['request']
        )


class APIAppSerializer(serializers.Serializer):
    app_name = serializers.CharField()
    url = serializers.SerializerMethodField()
    version_string = serializers.CharField()

    def get_url(self, instance):
        return reverse(
            'rest_api:api-version-1-app', args=(instance.app.name,),
            format=self.context['format'], request=self.context['request']
        )
