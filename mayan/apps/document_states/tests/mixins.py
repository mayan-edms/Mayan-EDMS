from __future__ import unicode_literals

from ..classes import WorkflowAction
from ..models import Workflow, WorkflowRuntimeProxy, WorkflowStateRuntimeProxy

from .literals import (
    TEST_WORKFLOW_INITIAL_STATE_LABEL, TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
    TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT, TEST_WORKFLOW_INTERNAL_NAME,
    TEST_WORKFLOW_LABEL, TEST_WORKFLOW_LABEL_EDITED,
    TEST_WORKFLOW_STATE_COMPLETION, TEST_WORKFLOW_STATE_LABEL,
    TEST_WORKFLOW_STATE_LABEL_EDITED, TEST_WORKFLOW_TRANSITION_LABEL,
    TEST_WORKFLOW_TRANSITION_LABEL_EDITED, TEST_WORKFLOW_TRANSITION_LABEL_2
)


class TestWorkflowAction(WorkflowAction):
    label = 'test workflow state action'


class WorkflowRuntimeProxyStateViewTestMixin(object):
    def _request_test_workflow_runtime_proxy_state_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_state_list',
            kwargs={'pk': self.test_workflow.pk}
        )

    def _request_test_workflow_runtime_proxy_state_document_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_state_document_list',
            kwargs={'pk': self.test_workflow_state_1.pk}
        )


class WorkflowRuntimeProxyViewTestMixin(object):
    def _request_test_workflow_runtime_proxy_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_list'
        )

    def _request_test_workflow_runtime_proxy_document_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_document_list',
            kwargs={'pk': self.test_workflow.pk}
        )


class WorkflowStateActionTestMixin(object):
    TestWorkflowAction = TestWorkflowAction
    test_workflow_state_action_path = 'mayan.apps.document_states.tests.mixins.TestWorkflowAction'

    def _create_test_workflow_state_action(self):
        self.test_workflow_state.actions.create(
            label=self.TestWorkflowAction.label,
            action_path=self.test_workflow_state_action_path
        )


class WorkflowStateViewTestMixin(object):
    def _request_test_workflow_state_create_view(self, extra_data=None):
        data = {
            'label': TEST_WORKFLOW_STATE_LABEL,
            'completion': TEST_WORKFLOW_STATE_COMPLETION,
        }
        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='document_states:workflow_template_state_create',
            kwargs={'pk': self.test_workflow.pk}, data=data
        )

    def _request_test_workflow_state_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_delete',
            kwargs={'pk': self.test_workflow_state_1.pk}
        )

    def _request_test_workflow_state_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_edit',
            kwargs={'pk': self.test_workflow_state_1.pk}, data={
                'label': TEST_WORKFLOW_STATE_LABEL_EDITED
            }
        )

    def _request_test_workflow_state_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_state_list',
            kwargs={'pk': self.test_workflow.pk}
        )


class WorkflowTestMixin(object):
    def _create_test_workflow(self, add_document_type=False):
        self.test_workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )
        self.test_workflow_runtime_proxy = WorkflowRuntimeProxy.objects.get(
            pk=self.test_workflow.pk
        )

        if add_document_type:
            self.test_workflow.document_types.add(self.test_document_type)

    def _create_test_workflow_state(self):
        self.test_workflow_state = self.test_workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )
        self.test_workflow_state_runtime_proxy = WorkflowStateRuntimeProxy.objects.get(
            pk=self.test_workflow_state.pk
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
        self.test_workflow_state_runtime_proxy_1 = WorkflowStateRuntimeProxy.objects.get(
            pk=self.test_workflow_state_1.pk
        )
        self.test_workflow_state_runtime_proxy_2 = WorkflowStateRuntimeProxy.objects.get(
            pk=self.test_workflow_state_2.pk
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


class WorkflowTransitionViewTestMixin(object):
    def _request_test_workflow_transition_create_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_create',
            kwargs={'pk': self.test_workflow.pk}, data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL,
                'origin_state': self.test_workflow_state_1.pk,
                'destination_state': self.test_workflow_state_2.pk,
            }
        )

    def _request_test_workflow_transition_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_delete',
            kwargs={'pk': self.test_workflow_transition.pk}
        )

    def _request_test_workflow_transition_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_edit',
            kwargs={'pk': self.test_workflow_transition.pk}, data={
                'label': TEST_WORKFLOW_TRANSITION_LABEL_EDITED,
                'origin_state': self.test_workflow_state_1.pk,
                'destination_state': self.test_workflow_state_2.pk,
            }
        )

    def _request_test_workflow_transition_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_list',
            kwargs={'pk': self.test_workflow.pk}
        )

    def _request_test_workflow_transition(self):
        return self.post(
            viewname='document_states:workflow_instance_transition_execute',
            kwargs={
                'workflow_instance_pk': self.test_workflow_instance.pk,
                'workflow_transition_pk': self.test_workflow_transition.pk,
            }
        )


class WorkflowViewTestMixin(object):
    def _request_test_workflow_create_view(self):
        return self.post(
            viewname='document_states:workflow_template_create', data={
                'label': TEST_WORKFLOW_LABEL,
                'internal_name': TEST_WORKFLOW_INTERNAL_NAME,
            }
        )

    def _request_test_workflow_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_delete', kwargs={
                'pk': self.test_workflow.pk
            }
        )

    def _request_test_workflow_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_edit', kwargs={
                'pk': self.test_workflow.pk,
            }, data={
                'label': TEST_WORKFLOW_LABEL_EDITED,
                'internal_name': self.test_workflow.internal_name
            }
        )

    def _request_test_workflow_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_list',
        )

    def _request_test_workflow_template_preview_view(self):
        return self.get(
            viewname='document_states:workflow_template_preview', kwargs={
                'pk': self.test_workflow.pk,
            }
        )
