import json

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.rest_api.relations import (
    FilteredPrimaryKeyRelatedField, MultiKwargHyperlinkedIdentityField
)
from mayan.apps.user_management.serializers import UserSerializer

from .models import (
    Workflow, WorkflowInstance, WorkflowInstanceLogEntry, WorkflowState,
    WorkflowTransition, WorkflowTransitionField
)


class WorkflowTemplateSerializer(serializers.HyperlinkedModelSerializer):
    document_types_add_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-document-type-add'
    )
    document_types_remove_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-document-type-remove'
    )
    document_types_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-document-type-list'
    )
    image_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-image'
    )
    states_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-state-list'
    )
    transitions_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-transition-list'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'workflow_template_id',
                'view_name': 'rest_api:workflow-template-detail'
            }
        }
        fields = (
            'document_types_add_url', 'document_types_remove_url',
            'document_types_url', 'id', 'image_url', 'internal_name',
            'label', 'states_url', 'transitions_url', 'url'
        )
        model = Workflow


class WorkflowTemplateDocumentTypeAddSerializer(serializers.Serializer):
    document_type_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the document type to add to the workflow.'
        ), source_model=DocumentType,
        source_permission=permission_document_type_edit
    )


class WorkflowTemplateDocumentTypeRemoveSerializer(serializers.Serializer):
    document_type_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the document type to remove from the workflow.'
        ), source_model=DocumentType,
        source_permission=permission_document_type_edit
    )


class WorkflowTemplateStateSerializer(serializers.HyperlinkedModelSerializer):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'workflow_template_state_id',
            }
        ),
        view_name='rest_api:workflow-template-state-detail'
    )
    workflow_template_url = serializers.HyperlinkedIdentityField(
        lookup_field='workflow_id', lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-detail'
    )

    class Meta:
        fields = (
            'completion', 'id', 'initial', 'label', 'url', 'workflow_template_url',
        )
        model = WorkflowState


class WorkflowTransitionFieldSerializer(serializers.HyperlinkedModelSerializer):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'transition.workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
            {
                'lookup_field': 'transition_id',
                'lookup_url_kwarg': 'workflow_template_transition_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'workflow_template_transition_field_id',
            }
        ),
        view_name='rest_api:workflow-template-transition-field-detail'
    )
    workflow_template_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'transition__workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
        ),
        view_name='rest_api:workflow-template-detail'
    )
    workflow_transition_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'transition.workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
            {
                'lookup_field': 'transition_id',
                'lookup_url_kwarg': 'workflow_template_transition_id',
            },
        ),
        view_name='rest_api:workflow-template-transition-detail'
    )

    class Meta:
        fields = (
            'field_type', 'name', 'help_text', 'id', 'label', 'required',
            'url', 'widget', 'widget_kwargs', 'workflow_template_url',
            'workflow_transition_url'
        )
        model = WorkflowTransitionField


class WorkflowTemplateTransitionSerializer(serializers.HyperlinkedModelSerializer):
    destination_state = WorkflowTemplateStateSerializer(read_only=True)
    destination_state_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the destination state to be added.'
        ), source_queryset_method='get_workflow_template_state_queryset'
    )
    field_list_url = serializers.SerializerMethodField()
    origin_state = WorkflowTemplateStateSerializer(read_only=True)
    origin_state_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the origin state to be added.'
        ), source_queryset_method='get_workflow_template_state_queryset'
    )
    url = serializers.SerializerMethodField()
    workflow_template_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'condition', 'destination_state', 'field_list_url', 'id', 'label',
            'origin_state', 'url', 'workflow_template_url',

            'destination_state_id',
            'origin_state_id'
        )
        model = WorkflowTransition
        read_only_fields = (
            'destination_state', 'field_list_url', 'id', 'origin_state',
            'url', 'workflow_template_url'
        )

    def create(self, validated_data):
        validated_data['destination_state'] = validated_data.pop(
            'destination_state_id'
        )
        validated_data['origin_state'] = validated_data.pop(
            'origin_state_id'
        )

        return super().create(
            validated_data=validated_data
        )

    def get_field_list_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-template-transition-field-list', kwargs={
                'workflow_template_id': instance.workflow_id,
                'workflow_template_transition_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-template-transition-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
                'workflow_template_transition_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_template_state_queryset(self):
        return self.context['external_object'].states.all()

    def get_workflow_template_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-template-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def update(self, instance, validated_data):
        validated_data['destination_state'] = validated_data.pop(
            'destination_state_id'
        )
        validated_data['origin_state'] = validated_data.pop(
            'origin_state_id'
        )

        return super().update(
            instance=instance, validated_data=validated_data
        )


class WorkflowInstanceLogEntrySerializer(serializers.ModelSerializer):
    document_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'workflow_instance.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
        ),
        view_name='rest_api:document-detail'
    )
    transition = WorkflowTemplateTransitionSerializer(read_only=True)
    transition_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the transition to be added.'
        ), source_queryset_method='get_workflow_instance_transition_queryset'
    )
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'workflow_instance.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'workflow_instance.pk',
                'lookup_url_kwarg': 'workflow_instance_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'workflow_instance_log_entry_id',
            }
        ),
        view_name='rest_api:workflow-instance-log-entry-detail'
    )
    user = UserSerializer(read_only=True)
    workflow_instance_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'workflow_instance.document.pk',
                'lookup_url_kwarg': 'document_id',
            },
            {
                'lookup_field': 'workflow_instance.pk',
                'lookup_url_kwarg': 'workflow_instance_id',
            }
        ),
        view_name='rest_api:workflow-instance-detail'
    )
    workflow_template_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'workflow_instance.workflow.pk',
                'lookup_url_kwarg': 'workflow_template_id'
            },
        ),
        view_name='rest_api:workflow-template-detail'
    )

    class Meta:
        fields = (
            'comment', 'datetime', 'document_url', 'extra_data', 'id',
            'transition', 'transition_id', 'url', 'user',
            'workflow_instance_url', 'workflow_template_url'
        )
        model = WorkflowInstanceLogEntry

    def create(self, validated_data):
        return self.context['workflow_instance'].do_transition(
            transition=validated_data['transition_id'],
            comment=validated_data.get('comment'),
            extra_data=json.loads(s=validated_data.get('extra_data', '{}')),
            user=self.context['request'].user
        )

    def get_workflow_instance_transition_queryset(self):
        return self.context['workflow_instance'].get_transition_choices(
            _user=self.context['request'].user
        )


class WorkflowInstanceSerializer(serializers.ModelSerializer):
    context = serializers.SerializerMethodField()
    current_state = WorkflowTemplateStateSerializer(
        read_only=True, source='get_current_state'
    )
    document_url = serializers.SerializerMethodField()
    last_log_entry = WorkflowInstanceLogEntrySerializer(
        read_only=True, source='get_last_log_entry'
    )
    log_entries_url = serializers.SerializerMethodField(
        help_text=_('A link to the entire history of this workflow.')
    )
    workflow_template_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(
        help_text=_(
            'API URL pointing to a workflow in relation to the '
            'document to which it is attached. This URL is different than '
            'the canonical workflow URL.'
        )
    )

    class Meta:
        fields = (
            'context', 'current_state', 'document_url', 'id',
            'last_log_entry', 'log_entries_url', 'url',
            'workflow_template_url'
        )
        model = WorkflowInstance

    def get_document_url(self, instance):
        return reverse(
            viewname='rest_api:document-detail', kwargs={
                'document_id': instance.document.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_context(self, instance):
        return {'workflow_instance_context': instance.loads()}

    def get_log_entries_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-instance-log-entry-list', kwargs={
                'document_id': instance.document.pk,
                'workflow_instance_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-instance-detail', kwargs={
                'document_id': instance.document.pk,
                'workflow_instance_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_template_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-template-detail', kwargs={
                'workflow_template_id': instance.workflow.pk
            }, request=self.context['request'], format=self.context['format']
        )
