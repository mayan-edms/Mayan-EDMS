from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from documents.models import DocumentType
from documents.serializers import DocumentTypeSerializer

from .models import Workflow, WorkflowState


class NewWorkflowDocumentTypeSerializer(serializers.Serializer):
    document_type_pk = serializers.IntegerField(
        help_text=_('Primary key of the document type to be added.')
    )

    def create(self, validated_data):
        document_type = DocumentType.objects.get(
            pk=validated_data['document_type_pk']
        )
        self.context['workflow'].document_types.add(document_type)

        return validated_data


class WorkflowDocumentTypeSerializer(DocumentTypeSerializer):
    workflow_document_type_url = serializers.SerializerMethodField(
        help_text=_(
            'API URL pointing to a document type in relation to the '
            'workflow to which it is attached. This URL is different than '
            'the canonical document type URL.'
        )
    )

    class Meta(DocumentTypeSerializer.Meta):
        fields = DocumentTypeSerializer.Meta.fields + (
            'workflow_document_type_url',
        )
        read_only_fields = DocumentTypeSerializer.Meta.fields

    def get_workflow_document_type_url(self, instance):
        return reverse(
            'rest_api:workflow-document-type-detail', args=(
                self.context['workflow'].pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )


class WorkflowStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:workflowstate-detail'},
            'workflow': {'view_name': 'rest_api:workflow-detail'},
        }
        fields = ('completion', 'id', 'initial', 'label', 'workflow', 'url')
        model = WorkflowState


class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    document_types_url = serializers.HyperlinkedIdentityField(
        view_name='rest_api:workflow-document-type-list'
    )
    states = WorkflowStateSerializer(many=True, required=False)

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:workflow-detail'},
        }
        fields = (
            'document_types_url', 'id', 'label', 'states', 'url'
        )
        model = Workflow


class WritableWorkflowSerializer(serializers.ModelSerializer):
    document_types_pk_list = serializers.CharField(
        help_text=_(
            'Comma separated list of document type primary keys to which this '
            'workflow will be attached.'
        ), required=False
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:workflow-detail'},
        }
        fields = (
            'document_types_pk_list', 'label', 'id', 'url',
        )
        model = Workflow

    def _add_document_types(self, document_types_pk_list, instance):
        instance.document_types.add(
            *DocumentType.objects.filter(
                pk__in=document_types_pk_list.split(',')
            )
        )

    def create(self, validated_data):
        document_types_pk_list = validated_data.pop(
            'document_types_pk_list', ''
        )

        instance = super(WritableWorkflowSerializer, self).create(
            validated_data
        )

        if document_types_pk_list:
            self._add_document_types(
                document_types_pk_list=document_types_pk_list,
                instance=instance
            )

        return instance

    def update(self, instance, validated_data):
        document_types_pk_list = validated_data.pop(
            'document_types_pk_list', ''
        )

        instance = super(WritableWorkflowSerializer, self).update(
            instance, validated_data
        )

        if document_types_pk_list:
            instance.documents.clear()
            self._add_documents(
                document_types_pk_list=document_types_pk_list,
                instance=instance
            )

        return instance
