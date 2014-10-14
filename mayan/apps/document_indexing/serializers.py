from __future__ import absolute_import

from rest_framework import serializers

from .models import Index, IndexInstanceNode, IndexTemplateNode



class IndexInstanceNodeSerializer(serializers.ModelSerializer):
    documents = serializers.HyperlinkedIdentityField(view_name='index-node-documents')

    class Meta:
        fields = ('id', 'parent', 'index_template_node', 'value', 'level', 'documents')
        model = IndexInstanceNode


class IndexTemplateNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexTemplateNode


class IndexSerializer(serializers.ModelSerializer):
    node_templates = IndexTemplateNodeSerializer(read_only=True, many=True)
    node_instances = IndexInstanceNodeSerializer(read_only=True, many=True)

    class Meta:
        model = Index
