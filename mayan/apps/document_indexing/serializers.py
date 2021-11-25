from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_recursive.fields import RecursiveField

from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.rest_api.relations import FilteredPrimaryKeyRelatedField

from .models import (
    IndexInstance, IndexInstanceNode, IndexTemplate, IndexTemplateNode
)


class IndexInstanceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    nodes_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('label', 'id', 'nodes_url', 'url')
        model = IndexInstance
        read_only_fields = fields

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
    children_url = serializers.SerializerMethodField(read_only=True)
    documents_url = serializers.SerializerMethodField(read_only=True)
    index_url = serializers.SerializerMethodField(read_only=True)
    parent_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'documents_url', 'children_url', 'id', 'index_url', 'level',
            'parent_id', 'parent_url', 'value', 'url'
        )
        model = IndexInstanceNode
        read_only_fields = fields

    def get_children_url(self, obj):
        return reverse(
            viewname='rest_api:indexinstancenode-children-list', kwargs={
                'index_instance_id': obj.index().pk,
                'index_instance_node_id': obj.pk
            }, format=self.context['format'], request=self.context['request']
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
        read_only_fields = (
            'children', 'id', 'index', 'index_url', 'level', 'parent_url',
            'url'
        )

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
    parent = FilteredPrimaryKeyRelatedField()
    parent_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'children', 'enabled', 'expression', 'id', 'index', 'index_url',
            'level', 'link_documents', 'parent', 'parent_url', 'url'
        )
        model = IndexTemplateNode
        read_only_fields = (
            'children', 'id', 'index', 'index_url', 'level', 'parent_url',
            'url'
        )

    def create(self, validated_data):
        validated_data['index'] = self.context['index_template']
        return super().create(validated_data=validated_data)

    def get_index_url(self, obj):
        return reverse(
            viewname='rest_api:indextemplate-detail', kwargs={
                'index_template_id': obj.index.pk,
            }, format=self.context['format'], request=self.context['request']
        )

    def get_parent_queryset(self):
        return self.context['index_template'].index_template_nodes.all()

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


class IndexTemplateSerializer(serializers.HyperlinkedModelSerializer):
    document_types_url = serializers.HyperlinkedIdentityField(
        help_text=_(
            'URL of the API endpoint showing the list document types '
            'associated with this index template.'
        ), lookup_url_kwarg='index_template_id',
        view_name='rest_api:indextemplate-documenttype-list'
    )
    document_types_add_url = serializers.HyperlinkedIdentityField(
        help_text=_(
            'URL of the API endpoint to add document types '
            'to this index template.'
        ), lookup_url_kwarg='index_template_id',
        view_name='rest_api:indextemplate-documenttype-add'
    )
    document_types_remove_url = serializers.HyperlinkedIdentityField(
        help_text=_(
            'URL of the API endpoint to remove document types '
            'from this index template.'
        ), lookup_url_kwarg='index_template_id',
        view_name='rest_api:indextemplate-documenttype-remove'
    )
    index_template_root_node_id = serializers.PrimaryKeyRelatedField(
        source='index_template_root_node', read_only=True
    )
    nodes_url = serializers.SerializerMethodField(read_only=True)
    rebuild_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='index_template_id',
        view_name='rest_api:indextemplate-rebuild',
    )
    reset_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='index_template_id',
        view_name='rest_api:indextemplate-reset',
    )
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        extra_kwargs = {
            'document_types': {
                'lookup_url_kwarg': 'document_type_id',
                'view_name': 'rest_api:documenttype-detail'
            },
        }
        fields = (
            'document_types_add_url', 'document_types_url',
            'document_types_remove_url', 'enabled', 'id',
            'index_template_root_node_id', 'label', 'nodes_url',
            'rebuild_url', 'reset_url', 'slug', 'url'
        )
        model = IndexTemplate
        read_only_fields = (
            'document_types_add_url', 'document_types_url',
            'document_types_remove_url', 'id', 'index_template_root_node_id',
            'nodes_url', 'rebuild_url', 'reset_url', 'url'
        )

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


class DocumentTypeAddSerializer(serializers.Serializer):
    document_type = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the document type to add to the index template.'
        ), source_model=DocumentType,
        source_permission=permission_document_type_edit
    )


class DocumentTypeRemoveSerializer(serializers.Serializer):
    document_type = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the document type to remove from the index template.'
        ), source_model=DocumentType,
        source_permission=permission_document_type_edit
    )
