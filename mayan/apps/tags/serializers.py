from __future__ import absolute_import

from rest_framework import serializers
from taggit.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    color = serializers.CharField(source='properties.get.color')

    class Meta:
        model = Tag
