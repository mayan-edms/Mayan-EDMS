from __future__ import absolute_import

from rest_framework import serializers

from .models import Folder


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    # FIXME: Doing a: from documents.serializers import DocumentSerializer
    # causes an unexplained ImportError, so we import it hidden until the issue
    # is resolved

    def __init__(self, *args, **kwargs):
        from documents.serializers import DocumentSerializer
        super(FolderSerializer, self).__init__(*args, **kwargs)
        self.fields['documents'] = DocumentSerializer()

    class Meta:
        fields = ('id', 'url', 'title', 'user', 'datetime_created')
        model = Folder
