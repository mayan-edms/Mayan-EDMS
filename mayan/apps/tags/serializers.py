from __future__ import absolute_import

from rest_framework import serializers
from taggit.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    color = serializers.CharField(source='properties.get.color')
    documents = serializers.HyperlinkedIdentityField(view_name='tag-document-list')

    class Meta:
        fields = ('id', 'url', 'name', 'color', 'slug', 'documents')
        model = Tag
