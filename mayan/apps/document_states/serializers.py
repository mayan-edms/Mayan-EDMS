import json

from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.serializers.document_type_serializers import DocumentTypeSerializer
from mayan.apps.user_management.serializers import UserSerializer

from .models import (
    Workflow, WorkflowInstance, WorkflowInstanceLogEntry, WorkflowState,
    WorkflowTransition, WorkflowTransitionField
)

#TODO:Add workflow document type add and remove views


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
        return super().create(validated_data)

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflowstate-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
                'workflow_template_state_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-detail', kwargs={
                'workflow_template_id': instance.workflow.pk
            }, request=self.context['request'], format=self.context['format']
        )


class WorkflowTransitionFieldSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    workflow_transition_url = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'workflow_transition_field_id',
                'view_name': 'rest_api:workflowtransitionfield-detail'
            },
        }
        fields = (
            'field_type', 'name', 'help_text', 'id', 'label', 'required',
            'url', 'widget', 'widget_kwargs', 'workflow_transition_url'
        )
        model = WorkflowTransitionField

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflowtransitionfield-detail', kwargs={
                'workflow_template_id': instance.transition.workflow_id,
                'workflow_template_transition_id': instance.transition_id,
                'workflow_template_transition_field_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_transition_url(self, instance):
        return reverse(
            viewname='rest_api:workflowtransition-detail', kwargs={
                'workflow_template_id': instance.transition.workflow_id,
                'workflow_template_transition_id': instance.transition_id,
            }, request=self.context['request'], format=self.context['format']
        )


class WorkflowTransitionFieldSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    workflow_transition_url = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'workflow_transition_field_id',
                'view_name': 'rest_api:workflowtransitionfield-detail'
            },
        }
        fields = (
            'field_type', 'name', 'help_text', 'id', 'label', 'required',
            'url', 'widget', 'widget_kwargs', 'workflow_transition_url'
        )
        model = WorkflowTransitionField

    def get_url(self, instance):
        return reverse(
            'rest_api:workflowtransitionfield-detail', kwargs={
                'workflow_template_id': instance.transition.workflow_id,
                'workflow_template_transition_id': instance.transition_id,
                'workflow_template_transition_field_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_transition_url(self, instance):
        return reverse(
            'rest_api:workflowtransition-detail', kwargs={
                'workflow_template_id': instance.transition.workflow_id,
                'workflow_template_transition_id': instance.transition_id,
            }, request=self.context['request'], format=self.context['format']
        )


class WorkflowTransitionSerializer(serializers.HyperlinkedModelSerializer):
    destination_state = WorkflowStateSerializer()
    field_list_url = serializers.SerializerMethodField()
    origin_state = WorkflowStateSerializer()
    url = serializers.SerializerMethodField()
    workflow_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'destination_state', 'field_list_url', 'id', 'label',
            'origin_state', 'url', 'workflow_url',
        )
        model = WorkflowTransition

    def get_field_list_url(self, instance):
        return reverse(
            viewname='rest_api:workflowtransitionfield-list', kwargs={
                'workflow_template_id': instance.workflow_id,
                'workflow_template_transition_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflowtransition-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
                'workflow_template_transition_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
            }, request=self.context['request'], format=self.context['format']
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
        return super().create(validated_data=validated_data)

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflowtransition-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
                'workflow_template_transition_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-detail', kwargs={
                'workflow_template_id': instance.workflow.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def update(self, instance, validated_data):
        validated_data['destination_state'] = WorkflowState.objects.get(
            pk=validated_data.pop('destination_state_pk')
        )
        validated_data['origin_state'] = WorkflowState.objects.get(
            pk=validated_data.pop('origin_state_pk')
        )

        return super().update(
            instance=instance, validated_data=validated_data
        )


class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    document_types_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-document-type-list'
    )
    image_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-image'
    )
    states_url = serializers.SerializerMethodField()
    transitions_url = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'workflow_template_id',
                'view_name': 'rest_api:workflow-detail'
            }
        }
        fields = (
            'document_types_url', 'id', 'image_url', 'internal_name',
            'label', 'states_url', 'transitions_url', 'url'
        )
        model = Workflow

    def get_states_url(self, instance):
        return reverse(
            viewname='rest_api:workflowstate-list', kwargs={
                'workflow_template_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_transitions_url(self, instance):
        return reverse(
            viewname='rest_api:workflowtransition-list', kwargs={
                'workflow_template_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )


#TODO: transition list from WorkflowInstanceTransitionSelectForm
#TODO: Add extra_data=extra_data
class WorkflowInstanceLogEntrySerializer(serializers.ModelSerializer):
    document_workflow_url = serializers.SerializerMethodField()
    transition = WorkflowTransitionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        fields = (
            'comment', 'datetime', 'document_workflow_url', 'transition',
            'user'
        )
        model = WorkflowInstanceLogEntry

    def get_document_workflow_url(self, instance):
        return reverse(
            viewname='rest_api:workflowinstance-detail', kwargs={
                'document_id': instance.workflow_instance.document.pk,
                'workflow_instance_id': instance.workflow_instance.pk
            }, request=self.context['request'], format=self.context['format']
        )


class WorkflowInstanceSerializer(serializers.ModelSerializer):
    context = serializers.SerializerMethodField()
    current_state = WorkflowStateSerializer(
        read_only=True, source='get_current_state'
    )
    document_url = serializers.SerializerMethodField()
    last_log_entry = WorkflowInstanceLogEntrySerializer(
        read_only=True, source='get_last_log_entry'
    )
    log_entries_url = serializers.SerializerMethodField(
        help_text=_('A link to the entire history of this workflow.')
    )
    transition_choices = WorkflowTransitionSerializer(
        many=True, read_only=True, source='get_transition_choices'
    )
    workflow_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(
        help_text=_(
            'API URL pointing to a workflow in relation to the '
            'document to which it is attached. This URL is different than '
            'the canonical workflow URL.'
        )
    )

    class Meta:
        fields = (
            'context', 'current_state', 'document_url', 'last_log_entry',
            'log_entries_url', 'transition_choices', 'url', 'workflow_url'
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
            viewname='rest_api:workflowinstancelogentry-list', kwargs={
                'document_id': instance.document.pk,
                'workflow_instance_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflowinstance-detail', kwargs={
                'document_id': instance.document.pk,
                'workflow_instance_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def get_workflow_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-detail', kwargs={
                'workflow_template_id': instance.workflow.pk
            }, request=self.context['request'], format=self.context['format']
        )


class WritableWorkflowInstanceLogEntrySerializer(serializers.ModelSerializer):
    transition_pk = serializers.IntegerField(
        help_text=_('Primary key of the transition to be added.'),
        write_only=True
    )
    transition = WorkflowTransitionSerializer(read_only=True)
    url = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        fields = (
            'comment', 'datetime', 'transition', 'transition_pk', 'user',
            'url'
        )
        model = WorkflowInstanceLogEntry

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:workflowinstance-detail', kwargs={
                'document_id': instance.workflow_instance.document.pk,
                'workflow_instance_id': instance.workflow_instance.pk
            }, request=self.context['request'], format=self.context['format']
        )

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['workflow_instance'] = self.context['workflow_instance']
        attrs['transition'] = WorkflowTransition.objects.get(
            pk=attrs.pop('transition_pk')
        )

        instance = WorkflowInstanceLogEntry(**attrs)

        try:
            instance.full_clean()
        except DjangoValidationError as exception:
            raise ValidationError(exception)

        return attrs
