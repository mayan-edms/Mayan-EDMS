from rest_framework import serializers


class APISerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()


class APIAppSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()


class APIVersionSerializer(serializers.Serializer):
    apps = APIAppSerializer()
