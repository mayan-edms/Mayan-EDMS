from __future__ import unicode_literals

from rest_framework import serializers

from user_management.serializers import UserSerializer

from .models import Folder


class FolderSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents_count')
    user = UserSerializer(read_only=True)

    class Meta:
        fields = ('datetime_created', 'documents', 'id', 'label', 'user')
        model = Folder

    def get_documents_count(self, obj):
        return obj.documents.count()
