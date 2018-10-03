from __future__ import unicode_literals

from ..models import Workflow, WorkflowState, WorkflowTransition

from .literals import (
    TEST_WORKFLOW_INITIAL_STATE_LABEL, TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
    TEST_WORKFLOW_INTERNAL_NAME, TEST_WORKFLOW_LABEL,
    TEST_WORKFLOW_STATE_LABEL, TEST_WORKFLOW_STATE_COMPLETION,
    TEST_WORKFLOW_TRANSITION_LABEL, TEST_WORKFLOW_TRANSITION_LABEL_2
)


class WorkflowTestMixin(object):
    def _create_workflow(self):
        self.workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )

    def _create_workflow_states(self):
        self.workflow_initial_state = WorkflowState.objects.create(
            workflow=self.workflow, label=TEST_WORKFLOW_INITIAL_STATE_LABEL,
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION, initial=True
        )
        self.workflow_state = WorkflowState.objects.create(
            workflow=self.workflow, label=TEST_WORKFLOW_STATE_LABEL,
            completion=TEST_WORKFLOW_STATE_COMPLETION
        )

    def _create_workflow_transition(self):
        self.workflow_transition = WorkflowTransition.objects.create(
            workflow=self.workflow, label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.workflow_initial_state,
            destination_state=self.workflow_state
        )

    def _create_workflow_transitions(self):
        self.workflow_transition = WorkflowTransition.objects.create(
            workflow=self.workflow, label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.workflow_initial_state,
            destination_state=self.workflow_state
        )

        self.workflow_transition_2 = WorkflowTransition.objects.create(
            workflow=self.workflow, label=TEST_WORKFLOW_TRANSITION_LABEL_2,
            origin_state=self.workflow_initial_state,
            destination_state=self.workflow_state
        )
