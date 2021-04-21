from django.db.models import Q

from ...models import WorkflowState, WorkflowStateAction

from ..literals import (
    DOCUMENT_WORKFLOW_LAUNCH_ACTION_CLASS_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_GENERIC_DOTTED_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN,
    TEST_WORKFLOW_TEMPLATE_STATE_COMPLETION,
    TEST_WORKFLOW_TEMPLATE_STATE_LABEL,
    TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
)
from ..workflow_actions import TestWorkflowAction


class WorkflowTemplateStateActionLaunchViewTestMixin:
    def _request_document_workflow_template_launch_action_create_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk,
                'class_path': DOCUMENT_WORKFLOW_LAUNCH_ACTION_CLASS_PATH
            }, data={
                'enabled': True,
                'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
                'when': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN,
                'workflows': self.test_workflow_templates[0].pk
            }
        )


class WorkflowTemplateStateActionTestMixin:
    TestWorkflowAction = TestWorkflowAction
    test_workflow_template_state_action_path = TEST_WORKFLOW_TEMPLATE_STATE_ACTION_GENERIC_DOTTED_PATH

    def setUp(self):
        super().setUp()
        self.test_workflow_template_state_actions = []

    def _create_test_workflow_template_state_action(
        self, extra_data=None, workflow_state_index=0
    ):
        total_test_workflow_template_state_actions = len(
            self.test_workflow_template_state_actions
        )
        label = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
            total_test_workflow_template_state_actions
        )

        data = {
            'label': label,
            'action_path': self.test_workflow_template_state_action_path
        }

        if extra_data:
            data.update(extra_data)

        self.test_workflow_template_state_action = self.test_workflow_template_states[
            workflow_state_index
        ].actions.create(
            **data
        )

        self.test_workflow_template_state_actions.append(
            self.test_workflow_template_state_action
        )


class WorkflowTemplateStateActionViewTestMixin:
    def _request_test_workflow_template_state_action_create_get_view(self, class_path):
        return self.get(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk,
                'class_path': class_path
            }
        )

    def _request_test_workflow_template_state_action_create_post_view(
        self, class_path, extra_data=None
    ):
        data = {
            'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
            'when': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN
        }
        if extra_data:
            data.update(extra_data)

        pk_list = list(
            WorkflowStateAction.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk,
                'class_path': class_path
            }, data=data
        )

        try:
            self.test_workflow_template_state_action = WorkflowStateAction.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowStateAction.DoesNotExist:
            self.test_workflow_template_state_action = None

        return response

    def _request_test_worflow_template_state_action_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_delete',
            kwargs={
                'workflow_template_state_action_id': self.test_workflow_template_state_action.pk
            }
        )

    def _request_test_worflow_template_state_action_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_edit',
            kwargs={
                'workflow_template_state_action_id': self.test_workflow_template_state_action.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED,
                'when': self.test_workflow_template_state_action.when
            }
        )

    def _request_test_worflow_template_state_action_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_state_action_list',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_template_state_action_selection_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_selection',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }, data={
                'klass': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
            }
        )


class WorkflowTemplateStateAPIViewTestMixin:
    def _request_test_workflow_template_state_create_api_view(self):
        pk_list = list(WorkflowState.objects.values('pk'))

        response = self.post(
            viewname='rest_api:workflow-template-state-list',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }, data={
                'completion': TEST_WORKFLOW_TEMPLATE_STATE_COMPLETION,
                'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL
            }
        )

        try:
            self.test_workflow_template_state = WorkflowState.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowState.DoesNotExist:
            self.test_workflow_template_state = None

        return response

    def _request_test_workflow_template_state_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_template_state_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_template_state_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-list', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_state_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
            }
        )

    def _request_test_workflow_template_state_edit_put_api_view(self):
        return self.put(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
            }
        )


class WorkflowStateViewTestMixin:
    def _request_test_workflow_template_state_create_view(self, extra_data=None):
        pk_list = list(WorkflowState.objects.values_list('pk', flat=True))

        data = {
            'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL,
            'completion': TEST_WORKFLOW_TEMPLATE_STATE_COMPLETION,
        }
        if extra_data:
            data.update(extra_data)

        response = self.post(
            viewname='document_states:workflow_template_state_create',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }, data=data
        )

        try:
            self.test_workflow_template_state = WorkflowState.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowState.DoesNotExist:
            self.test_workflow_template_state = None

        return response

    def _request_test_workflow_template_state_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_delete',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_states[0].pk
            }
        )

    def _request_test_workflow_template_state_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_edit',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_states[0].pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
            }
        )

    def _request_test_workflow_template_state_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_state_list',
            kwargs={'workflow_template_id': self.test_workflow_template.pk}
        )
