from __future__ import absolute_import

from rest_framework import serializers
from taggit.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    # FIXME: Doing a: from documents.serializers import DocumentSerializer
    # causes an unexplained ImportError, so we import it hidden until the issue
    # is resolved

    def __init__(self, *args, **kwargs):
        from documents.serializers import DocumentSerializer
        super(TagSerializer, self).__init__(*args, **kwargs)
        self.fields['documents'] = DocumentSerializer()

    color = serializers.CharField(source='properties.get.color')

    class Meta:
        model = Tag
