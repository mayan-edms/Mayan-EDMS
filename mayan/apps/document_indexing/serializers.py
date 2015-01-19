from __future__ import unicode_literals

from rest_framework import serializers

from .models import Index, IndexInstanceNode, IndexTemplateNode


class IndexInstanceNodeSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField('get_documents_count')

    class Meta:
        fields = ('id', 'parent', 'value', 'level', 'documents', 'children')
        model = IndexInstanceNode

    def get_documents_count(self, obj):
        return obj.documents.count()


IndexInstanceNodeSerializer.base_fields['children'] = IndexInstanceNodeSerializer(many=True)


class IndexTemplateNodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'parent', 'index', 'expression', 'enabled', 'link_documents', 'level')
        model = IndexTemplateNode


class IndexSerializer(serializers.ModelSerializer):
    node_templates = IndexTemplateNodeSerializer(read_only=True, many=True)
    instance_root = IndexInstanceNodeSerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'title', 'enabled', 'document_types', 'node_templates', 'instance_root')
        model = Index
