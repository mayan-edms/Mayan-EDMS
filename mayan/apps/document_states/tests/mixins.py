from __future__ import unicode_literals

from ..models import Workflow

from .literals import (
    TEST_WORKFLOW_INITIAL_STATE_LABEL, TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
    TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT, TEST_WORKFLOW_INTERNAL_NAME,
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_COMPLETION, TEST_WORKFLOW_TRANSITION_LABEL,
    TEST_WORKFLOW_TRANSITION_LABEL_2
)


class WorkflowTestMixin(object):
    def _create_test_workflow(self, add_document_type=False):
        self.test_workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )

        if add_document_type:
            self.test_workflow.document_types.add(self.test_document_type)

    def _create_test_workflow_state(self):
        self.test_workflow_state = self.test_workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _create_test_workflow_states(self):
        self.test_workflow_state_1 = self.test_workflow.states.create(
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
            initial=True, label=TEST_WORKFLOW_INITIAL_STATE_LABEL
        )
        self.test_workflow_state_2 = self.test_workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _create_test_workflow_transition(self):
        self.test_workflow_transition = self.test_workflow.transitions.create(
            label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.test_workflow_state_1,
            destination_state=self.test_workflow_state_2,
        )

    def _create_test_workflow_transitions(self):
        self.test_workflow_transition = self.test_workflow.transitions.create(
            workflow=self.test_workflow, label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.test_workflow_state_1,
            destination_state=self.test_workflow_state_2
        )

        self.test_workflow_transition_2 = self.test_workflow.transitions.create(
            workflow=self.test_workflow, label=TEST_WORKFLOW_TRANSITION_LABEL_2,
            origin_state=self.test_workflow_state_1,
            destination_state=self.test_workflow_state_2
        )

    def _create_test_workflow_instance_log_entry(self):
        self.test_document.workflows.first().log_entries.create(
            comment=TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT,
            transition=self.test_workflow_transition,
            user=self._test_case_user
        )
