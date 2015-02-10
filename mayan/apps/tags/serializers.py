from __future__ import unicode_literals

from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents_count')

    class Meta:
        fields = ('id', 'label', 'color', 'documents')
        model = Tag

    def get_documents_count(self, obj):
        return obj.documents.count()
