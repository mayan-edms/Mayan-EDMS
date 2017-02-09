from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from documents.models import DocumentType
from documents.serializers import DocumentTypeSerializer

from .models import Workflow, WorkflowState, WorkflowTransition


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
    url = serializers.SerializerMethodField()
    workflow_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'completion', 'id', 'initial', 'label', 'url', 'workflow_url',
        )
        model = WorkflowState

    def create(self, validated_data):
        validated_data['workflow'] = self.context['workflow']
        return super(WorkflowStateSerializer, self).create(validated_data)

    def get_url(self, instance):
        return reverse(
            'rest_api:workflowstate-detail', args=(
                instance.workflow.pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            'rest_api:workflow-detail', args=(
                instance.workflow.pk,
            ), request=self.context['request'], format=self.context['format']
        )


class WorkflowTransitionSerializer(serializers.HyperlinkedModelSerializer):
    destination_state = WorkflowStateSerializer()
    origin_state = WorkflowStateSerializer()
    url = serializers.SerializerMethodField()
    workflow_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'destination_state', 'id', 'label', 'origin_state', 'url',
            'workflow_url',
        )
        model = WorkflowTransition

    def get_url(self, instance):
        return reverse(
            'rest_api:workflowtransition-detail', args=(
                instance.workflow.pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            'rest_api:workflow-detail', args=(
                instance.workflow.pk,
            ), request=self.context['request'], format=self.context['format']
        )


class WritableWorkflowTransitionSerializer(serializers.ModelSerializer):
    destination_state_pk = serializers.IntegerField(
        help_text=_('Primary key of the destination state to be added.'),
        write_only=True
    )
    origin_state_pk = serializers.IntegerField(
        help_text=_('Primary key of the origin state to be added.'),
        write_only=True
    )
    url = serializers.SerializerMethodField()
    workflow_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'destination_state_pk', 'id', 'label', 'origin_state_pk', 'url',
            'workflow_url',
        )
        model = WorkflowTransition

    def create(self, validated_data):
        validated_data['destination_state'] = WorkflowState.objects.get(
            pk=validated_data.pop('destination_state_pk')
        )
        validated_data['origin_state'] = WorkflowState.objects.get(
            pk=validated_data.pop('origin_state_pk')
        )

        validated_data['workflow'] = self.context['workflow']
        return super(WritableWorkflowTransitionSerializer, self).create(
            validated_data
        )

    def get_url(self, instance):
        return reverse(
            'rest_api:workflowtransition-detail', args=(
                instance.workflow.pk, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            'rest_api:workflow-detail', args=(
                instance.workflow.pk,
            ), request=self.context['request'], format=self.context['format']
        )

    def update(self, instance, validated_data):
        validated_data['destination_state'] = WorkflowState.objects.get(
            pk=validated_data.pop('destination_state_pk')
        )
        validated_data['origin_state'] = WorkflowState.objects.get(
            pk=validated_data.pop('origin_state_pk')
        )

        return super(WritableWorkflowTransitionSerializer, self).update(
            instance, validated_data
        )


class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    document_types_url = serializers.HyperlinkedIdentityField(
        view_name='rest_api:workflow-document-type-list'
    )
    states = WorkflowStateSerializer(many=True, required=False)
    transitions = WorkflowTransitionSerializer(many=True, required=False)

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:workflow-detail'},
        }
        fields = (
            'document_types_url', 'id', 'label', 'states', 'transitions',
            'url'
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
