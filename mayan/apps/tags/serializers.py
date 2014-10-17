from __future__ import absolute_import

from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedIdentityField(view_name='tag-document-list')

    class Meta:
        fields = ('id', 'url', 'label', 'color', 'documents')
        model = Tag
