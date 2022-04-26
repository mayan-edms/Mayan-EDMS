from django.db.models import Q

from ...models.workflow_state_escalation_models import WorkflowStateEscalation
from ...tasks import (
    task_workflow_instance_check_escalation,
    task_workflow_instance_check_escalation_all
)

from ..literals import (
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_AMOUNT,
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_AMOUNT_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_COMMENT,
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_UNIT
)


class WorkflowTemplateStateEscalationAPIViewTestMixin:
    def _request_test_workflow_template_state_escalation_create_api_view(self):
        data = {
            'amount': 1,
            'enabled': True,
            'workflow_template_transition_id': self._test_workflow_template_transition.pk
        }

        pk_list = list(
            WorkflowStateEscalation.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='rest_api:workflow-template-state-escalation-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_states[0].pk
            }, data=data
        )

        try:
            self._test_workflow_estate_escalation = WorkflowStateEscalation.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowStateEscalation.DoesNotExist:
            self._test_workflow_estate_escalation = None

        return response

    def _request_test_workflow_template_state_escalation_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-state-escalation-detail', kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_states[0].pk,
                'workflow_template_state_escalation_id': self._test_workflow_template_state_escalation.pk
            }
        )

    def _request_test_workflow_template_state_escalation_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-escalation-detail', kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_states[0].pk,
                'workflow_template_state_escalation_id': self._test_workflow_template_state_escalation.pk
            }
        )

    def _request_test_workflow_template_state_escalation_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-state-escalation-detail', kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_states[0].pk,
                'workflow_template_state_escalation_id': self._test_workflow_template_state_escalation.pk
            }, data={
                'amount': TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_AMOUNT_EDITED
            }
        )

    def _request_test_workflow_template_state_escalation_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:workflow-template-state-escalation-detail', kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_states[0].pk,
                'workflow_template_state_escalation_id': self._test_workflow_template_state_escalation.pk
            }, data={
                'amount': TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_AMOUNT_EDITED,
                'workflow_template_transition_id': self._test_workflow_template_transitions[0].pk
            }
        )

    def _request_test_workflow_template_state_escalation_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-escalation-list',
            kwargs={
                'workflow_template_id': self._test_workflow_template.pk,
                'workflow_template_state_id': self._test_workflow_template_states[0].pk
            }
        )


class WorkflowTemplateStateEscalationTaskTestMixin:
    def _execute_task_workflow_instance_check_escalation(
        self, test_workflow_instance_id
    ):
        task_workflow_instance_check_escalation.apply_async(
            kwargs={
                'workflow_instance_id': test_workflow_instance_id
            }
        ).get()

    def _execute_task_workflow_instance_check_escalation_all(self):
        task_workflow_instance_check_escalation_all.apply_async().get()


class WorkflowTemplateStateEscalationTestMixin:
    def _create_test_workflow_template_state_escalation(self, extra_data=None):
        kwargs = {
            'amount': TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_AMOUNT,
            'comment': TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_COMMENT,
            'transition': self._test_workflow_template_transition,
            'unit': TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_UNIT
        }

        if extra_data:
            kwargs.update(extra_data)

        self._test_workflow_template_state_escalation = self._test_workflow_template_states[0].escalations.create(
            **kwargs
        )
