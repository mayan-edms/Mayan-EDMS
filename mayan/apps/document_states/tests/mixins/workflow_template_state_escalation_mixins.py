from .literals import (
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_AMOUNT,
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_COMMENT,
    TEST_WORKFLOW_TEMPLATE_STATE_ESCALATION_UNIT
)


class WorkflowTemplateStateEscalationModelTestMixin:
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
