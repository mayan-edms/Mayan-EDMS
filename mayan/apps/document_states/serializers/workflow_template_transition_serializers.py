from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from mayan.apps.events.classes import EventType
from mayan.apps.events.serializers import EventTypeSerializer
from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import (
    FilteredPrimaryKeyRelatedField, MultiKwargHyperlinkedIdentityField
)

from ..models import (
    WorkflowTransition, WorkflowTransitionField,
    WorkflowTransitionTriggerEvent
)

from .workflow_template_state_serializers import WorkflowTemplateStateSerializer


class WorkflowTransitionFieldSerializer(
    serializers.HyperlinkedModelSerializer
):
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
    workflow_transition_id = serializers.IntegerField(
        read_only=True, source='transition_id'
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
            'workflow_transition_id', 'workflow_transition_url'
        )
        model = WorkflowTransitionField
        read_only_fields = (
            'id', 'url', 'workflow_template_url', 'workflow_transition_id',
            'workflow_transition_url'
        )


class WorkflowTemplateTransitionSerializer(
    serializers.HyperlinkedModelSerializer
):
    destination_state = WorkflowTemplateStateSerializer(read_only=True)
    destination_state_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the destination state to be added.'
        ), source_queryset_method='get_workflow_template_state_queryset',
        write_only=True
    )
    field_list_url = serializers.SerializerMethodField()
    origin_state = WorkflowTemplateStateSerializer(read_only=True)
    origin_state_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the origin state to be added.'
        ), source_queryset_method='get_workflow_template_state_queryset',
        write_only=True
    )
    trigger_list_url = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    workflow_template_id = serializers.IntegerField(
        read_only=True, source='workflow_id'
    )
    workflow_template_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'condition', 'destination_state', 'destination_state_id',
            'field_list_url', 'id', 'label', 'origin_state',
            'origin_state_id', 'trigger_list_url', 'url',
            'workflow_template_id', 'workflow_template_url'
        )
        model = WorkflowTransition
        read_only_fields = (
            'field_list_url', 'id', 'trigger_list_url', 'url',
            'workflow_template_id', 'workflow_template_url'
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
            viewname='rest_api:workflow-template-transition-field-list',
            kwargs={
                'workflow_template_id': instance.workflow_id,
                'workflow_template_transition_id': instance.pk,
            }, request=self.context['request'], format=self.context['format']
        )

    def get_trigger_list_url(self, instance):
        return reverse(
            viewname='rest_api:workflow-template-transition-trigger-list',
            kwargs={
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
        return self.context['workflow_template'].states.all()

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


class WorkflowTemplateTransitionTriggerSerializer(
    serializers.HyperlinkedModelSerializer
):
    event_type = EventTypeSerializer(read_only=True)
    event_type_id = serializers.CharField(
        label=_('Event Type ID'), source='event_type.event_type.id',
        write_only=True
    )
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
                'lookup_url_kwarg': 'workflow_template_transition_trigger_id',
            }
        ),
        view_name='rest_api:workflow-template-transition-trigger-detail'
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
    workflow_transition_id = serializers.IntegerField(
        read_only=True, source='transition_id'
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
            'event_type', 'event_type_id', 'id', 'url', 'workflow_template_url',
            'workflow_transition_id', 'workflow_transition_url'
        )
        model = WorkflowTransitionTriggerEvent
        read_only_fields = (
            'id', 'url', 'workflow_template_url', 'workflow_transition_id',
            'workflow_transition_url'
        )

    def create(self, validated_data):
        # Unroll nested source "event_type.event_type.id".
        event_type = validated_data.pop('event_type', None)
        event_type = event_type.get('event_type', {})
        event_type_id = event_type.get('id')

        if event_type_id:
            validated_data['event_type'] = EventType.get(
                id=event_type_id
            ).get_stored_event_type()

        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        # Unroll nested source "event_type.event_type.id".
        event_type = validated_data.pop('event_type', None)
        event_type = event_type.get('event_type', {})
        event_type_id = event_type.get('id')

        if event_type_id:
            validated_data['event_type'] = EventType.get(
                id=event_type_id
            ).get_stored_event_type()

        return super().update(
            instance=instance, validated_data=validated_data
        )

    def validate_event_type_id(self, data):
        try:
            EventType.get(id=data)
        except KeyError:
            raise ValidationError(
                _('Unknown or invalid event type ID `%s`') % data
            )
        else:
            return data
