from __future__ import unicode_literals

from rest_framework import serializers

from .models import Folder


class FolderSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents_count')

    class Meta:
        fields = ('id', 'title', 'user', 'datetime_created', 'documents')
        model = Folder
        read_only_fields = ('user',)

    def get_documents_count(self, obj):
        return obj.documents.count()
