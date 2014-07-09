from __future__ import absolute_import

from django.contrib.auth.models import Group, User

from rest_framework import serializers
from rest_framework.reverse import reverse


class APISerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()


class APIAppSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()


class APIVersionSerializer(serializers.Serializer):
    apps = APIAppSerializer()

