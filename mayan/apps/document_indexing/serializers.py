from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework_recursive.fields import RecursiveField

from .models import Index, IndexInstance, IndexInstanceNode, IndexTemplateNode


class IndexInstanceSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField(read_only=True)
    node_count = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    nodes_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'label', 'id', 'item_count', 'node_count', 'nodes_url', 'url'
        )
        model = IndexInstance

    def get_item_count(self, obj):
        return obj.get_item_count(user=self.context['request'])

    def get_node_count(self, obj):
        return obj.get_instance_node_count()

    def get_url(self, obj):
        return reverse(
            viewname='rest_api:indexinstance-detail', kwargs={
                'index_instance_id': obj.pk,
            }, format=self.context['format'], request=self.context['request']
        )

    def get_nodes_url(self, obj):
        return reverse(
            viewname='rest_api:indexinstancenode-list', kwargs={
                'index_instance_id': obj.pk,
            }, format=self.context['format'], request=self.context['request']
        )


class IndexInstanceNodeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    documents_count = serializers.SerializerMethodField()
    documents_url = serializers.SerializerMethodField(read_only=True)
    index_url = serializers.SerializerMethodField(read_only=True)
    parent_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'documents_count', 'documents_url', 'children', 'id',
            'index_url', 'level', 'parent', 'parent_url', 'value', 'url'
        )
        model = IndexInstanceNode

    def get_documents_count(self, obj):
        return obj.get_descendants_document_count(
            user=self.context['request'].user
        )

    def get_documents_url(self, obj):
        return reverse(
            viewname='rest_api:indexinstancenode-document-list', kwargs={
                'index_instance_id': obj.index().pk,
                'index_instance_node_id': obj.pk
            }, format=self.context['format'], request=self.context['request']
        )

    def get_index_url(self, obj):
        return reverse(
            viewname='rest_api:indexinstance-detail', kwargs={
                'index_instance_id': obj.index().pk,
            }, format=self.context['format'], request=self.context['request']
        )

    def get_parent_url(self, obj):
        if obj.parent:
            return reverse(
                viewname='rest_api:indexinstancenode-detail', kwargs={
                    'index_instance_id': obj.index().pk,
                    'index_instance_node_id': obj.parent.pk
                }, format=self.context['format'],
                request=self.context['request']
            )
        else:
            return ''

    def get_url(self, obj):
        return reverse(
            viewname='rest_api:indexinstancenode-detail', kwargs={
                'index_instance_id': obj.index().pk,
                'index_instance_node_id': obj.pk
            }, format=self.context['format'], request=self.context['request']
        )


class IndexTemplateNodeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    index_url = serializers.SerializerMethodField(read_only=True)
    parent_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'children', 'enabled', 'expression', 'id', 'index', 'index_url',
            'level', 'link_documents', 'parent', 'parent_url', 'url'
        )
        model = IndexTemplateNode
        read_only_fields = ('children', 'id', 'index', 'level')

    def get_index_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': obj.index.pk,
            }, format=self.context['format'], request=self.context['request']
        )

    def get_parent_url(self, obj):
        if obj.parent:
            return reverse(
                viewname='rest_api:indextemplatenode-detail', kwargs={
                    'index_template_id': obj.index.pk,
                    'index_template_node_id': obj.parent.pk
                }, format=self.context['format'],
                request=self.context['request']
            )
        else:
            return ''

    def get_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': obj.index.pk,
                'index_template_node_id': obj.pk
            }, format=self.context['format'], request=self.context['request']
        )


class IndexTemplateNodeWriteSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)
    index_url = serializers.SerializerMethodField(read_only=True)
    parent_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'children', 'enabled', 'expression', 'id', 'index', 'index_url',
            'level', 'link_documents', 'parent', 'parent_url', 'url'
        )
        model = IndexTemplateNode
        read_only_fields = ('children', 'id', 'index', 'level')

    def create(self, validated_data):
        validated_data['index'] = self.context['index_template']
        return super().create(validated_data=validated_data)

    def get_index_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': obj.index.pk,
            }, format=self.context['format'], request=self.context['request']
        )

    def get_parent_url(self, obj):
        if obj.parent:
            return reverse(
                viewname='rest_api:indextemplatenode-detail', kwargs={
                    'index_template_id': obj.index.pk,
                    'index_template_node_id': obj.parent.pk
                }, format=self.context['format'],
                request=self.context['request']
            )
        else:
            return ''

    def get_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplatenode-detail', kwargs={
                'index_template_id': obj.index.pk,
                'index_template_node_id': obj.pk
            }, format=self.context['format'], request=self.context['request']
        )

    def validate(self, attrs):
        parent = attrs.get('parent', None)
        if not parent:
            raise ValidationError(
                {'parent': [_('Parent cannot be empty.')]}
            )
        else:
            if not self.context['index_template'].node_templates.filter(id=parent.pk).exists():
                raise ValidationError(
                    {
                        'parent': [
                            _('Parent must be from the same index template.')
                        ]
                    }
                )

        return attrs


class IndexTemplateSerializer(serializers.HyperlinkedModelSerializer):
    nodes_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        extra_kwargs = {
            'document_types': {'view_name': 'rest_api:documenttype-detail'},
        }
        fields = (
            'document_types', 'enabled', 'id', 'label', 'nodes_url', 'slug',
            'url'
        )
        model = Index

    def get_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': obj.pk,
            }, format=self.context['format'], request=self.context['request']
        )

    def get_nodes_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplatenode-list', kwargs={
                'index_template_id': obj.pk,
            }, format=self.context['format'], request=self.context['request']
        )


class IndexTemplateWriteSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'document_types', 'enabled', 'label', 'id',
            'slug', 'url'
        )
        model = Index
        read_only_fields = ('id',)

    def get_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': obj.pk,
            }, format=self.context['format'], request=self.context['request']
        )
