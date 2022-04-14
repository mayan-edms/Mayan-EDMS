from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError

from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import (
    FilteredPrimaryKeyRelatedField, MultiKwargHyperlinkedIdentityField
)

from ..models.workflow_state_escalation_models import WorkflowStateEscalation


class WorkflowTemplateStateEscalationSerializer(serializers.HyperlinkedModelSerializer):
    url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'state__workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
            {
                'lookup_field': 'state_id',
                'lookup_url_kwarg': 'workflow_template_state_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'workflow_template_state_escalation_id',
            }
        ),
        view_name='rest_api:workflow-template-state-escalation-detail'
    )
    workflow_template_state_id = serializers.IntegerField(
        read_only=True, source='state_id'
    )
    workflow_template_state_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'state__workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
            {
                'lookup_field': 'state_id',
                'lookup_url_kwarg': 'workflow_template_state_id',
            }
        ),
        view_name='rest_api:workflow-template-state-detail'
    )
    workflow_template_transition_id = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the workflow template transition to be added.'
        ), label=_('Workflow template transition ID'),
        source='transition_id',
        source_queryset_method='get_workflow_template_transition_queryset'
    )
    workflow_template_transition_url = MultiKwargHyperlinkedIdentityField(
        view_kwargs=(
            {
                'lookup_field': 'transition__workflow_id',
                'lookup_url_kwarg': 'workflow_template_id',
            },
            {
                'lookup_field': 'transition_id',
                'lookup_url_kwarg': 'workflow_template_transition_id',
            }
        ),
        view_name='rest_api:workflow-template-transition-detail'
    )

    class Meta:
        fields = (
            'amount', 'comment', 'condition', 'enabled', 'id', 'priority',
            'url', 'unit', 'workflow_template_state_id',
            'workflow_template_state_url', 'workflow_template_transition_id',
            'workflow_template_transition_url'
        )
        model = WorkflowStateEscalation
        read_only_fields = (
            'id', 'url', 'workflow_template_state_id',
            'workflow_template_state_url',
            'workflow_template_transition_url'
        )

    def create(self, validated_data):
        validated_data['transition'] = validated_data.pop(
            'transition_id'
        )

        return super().create(
            validated_data=validated_data
        )

    def get_workflow_template_transition_queryset(self):
        return self.context['workflow_template'].transitions.all()

    def update(self, instance, validated_data):
        if 'transition_id' in validated_data:
            validated_data['transition'] = validated_data.pop(
                'transition_id'
            )

        return super().update(
            instance=instance, validated_data=validated_data
        )

    def validate(self, attrs):
        if self.instance:
            return attrs

        kwargs = attrs.copy()
        kwargs['state'] = self.context['workflow_template_state']
        kwargs['transition_id'] = attrs['transition_id'].pk

        instance = WorkflowStateEscalation(**kwargs)
        try:
            instance.full_clean()
        except DjangoValidationError as exception:
            raise ValidationError(exception)

        return attrs
