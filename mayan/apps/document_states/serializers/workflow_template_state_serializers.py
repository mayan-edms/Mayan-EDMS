from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from ..models import WorkflowState, WorkflowStateAction


class WorkflowTemplateStateSerializer(serializers.HyperlinkedModelSerializer):
    actions_url = MultiKwargHyperlinkedIdentityField(
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
        view_name='rest_api:workflow-template-state-action-list'
    )
    escalations_url = MultiKwargHyperlinkedIdentityField(
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
        view_name='rest_api:workflow-template-state-escalation-list'
    )
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
    workflow_template_id = serializers.IntegerField(
        read_only=True, source='workflow_id'
    )
    workflow_template_url = serializers.HyperlinkedIdentityField(
        lookup_field='workflow_id', lookup_url_kwarg='workflow_template_id',
        view_name='rest_api:workflow-template-detail'
    )

    class Meta:
        fields = (
            'actions_url', 'completion', 'escalations_url', 'id', 'initial',
            'label', 'url',
            'workflow_template_id', 'workflow_template_url'
        )
        model = WorkflowState
        read_only_fields = (
            'escalations_url', 'id', 'url', 'workflow_template_id',
            'workflow_template_url'
        )


class WorkflowTemplateStateActionSerializer(serializers.HyperlinkedModelSerializer):
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
                'lookup_url_kwarg': 'workflow_template_state_action_id',
            }
        ),
        view_name='rest_api:workflow-template-state-action-detail'
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

    class Meta:
        fields = (
            'action_path', 'action_data', 'condition', 'enabled', 'id',
            'label', 'url', 'when', 'workflow_template_state_id',
            'workflow_template_state_url'
        )
        model = WorkflowStateAction
        read_only_fields = (
            'id', 'url', 'workflow_template_state_id',
            'workflow_template_state_url'
        )
