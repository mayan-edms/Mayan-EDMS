from __future__ import absolute_import

from rest_framework import serializers

from .models import Folder


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedIdentityField(view_name='folder-document-list')

    class Meta:
        fields = ('id', 'url', 'title', 'user', 'datetime_created', 'documents')
        model = Folder
