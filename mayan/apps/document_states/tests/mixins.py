from django.db.models import Q

from ..classes import WorkflowAction
from ..models import (
    Workflow, WorkflowRuntimeProxy, WorkflowState, WorkflowStateAction,
    WorkflowStateRuntimeProxy, WorkflowTransition, WorkflowTransitionField
)

from .literals import (
    DOCUMENT_WORKFLOW_LAUNCH_ACTION_CLASS_PATH,
    TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT,
    TEST_WORKFLOW_TEMPLATE_INTERNAL_NAME,
    TEST_WORKFLOW_TEMPLATE_LABEL, TEST_WORKFLOW_TEMPLATE_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
    TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN,
    TEST_WORKFLOW_TEMPLATE_STATE_COMPLETION,
    TEST_WORKFLOW_TEMPLATE_STATE_LABEL,
    TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
)


class DocumentTypeAddRemoveWorkflowTemplateViewTestMixin:
    def _request_test_document_type_workflow_template_add_remove_get_view(self):
        return self.get(
            viewname='document_states:document_type_workflow_templates',
            kwargs={
                'document_type_id': self.test_document_type.pk,
            }
        )

    def _request_test_document_type_workflow_template_add_view(self):
        return self.post(
            viewname='document_states:document_type_workflow_templates',
            kwargs={
                'document_type_id': self.test_document_type.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_workflow_template.pk
            }
        )

    def _request_test_document_type_workflow_template_remove_view(self):
        return self.post(
            viewname='document_states:document_type_workflow_templates',
            kwargs={
                'document_type_id': self.test_document_type.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_workflow_template.pk
            }
        )


class WorkflowTemplateDocumentTypeViewTestMixin:
    def _request_test_workflow_template_document_type_add_remove_get_view(self):
        return self.get(
            viewname='document_states:workflow_template_document_types',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_document_type_add_view(self):
        return self.post(
            viewname='document_states:workflow_template_document_types',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_document_type.pk
            }
        )

    def _request_test_workflow_template_document_type_remove_view(self):
        return self.post(
            viewname='document_states:workflow_template_document_types',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_document_type.pk
            }
        )


class WorkflowInstanceAPIViewTestMixin:
    def _request_test_workflow_instance_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-instance-detail', kwargs={
                'document_id': self.test_document.pk,
                'workflow_instance_id': self.test_document.workflows.first().pk
            }
        )

    def _request_test_workflow_instance_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-instance-list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_workflow_instance_log_entry_create_api_view(self, workflow_instance, extra_data=None):
        data = {
            'transition_id': self.test_workflow_template_transition.pk
        }

        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='rest_api:workflow-instance-log-entry-list', kwargs={
                'document_id': self.test_document.pk,
                'workflow_instance_id': workflow_instance.pk
            }, data=data
        )

    def _request_test_workflow_instance_log_entry_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-instance-log-entry-list', kwargs={
                'document_id': self.test_document.pk,
                'workflow_instance_id': self.test_document.workflows.first().pk
            }
        )


class WorkflowTemplateLaunchActionViewTestMixin:
    def _request_document_workflow_template_launch_action_create_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_create',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk,
                'class_path': DOCUMENT_WORKFLOW_LAUNCH_ACTION_CLASS_PATH
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_LABEL,
                'when': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_WHEN,
                'workflows': self.test_workflow_template.pk
            }
        )


class DocumentWorkflowTemplateViewTestMixin:
    def _request_test_document_single_workflow_template_launch_view(self):
        return self.post(
            viewname='document_states:document_single_workflow_templates_launch',
            kwargs={
                'document_id': self.test_document.pk
            }, data={
                'workflows': self.test_workflow_template.pk
            }
        )


class TestWorkflowAction(WorkflowAction):
    label = 'test workflow state action'

    def execute(self, context):
        context['workflow_instance']._workflow_state_action_executed = True


class WorkflowTemplateAPIViewTestMixin:
    def _request_test_workflow_template_create_api_view(self, extra_data=None):
        data = {
            'internal_name': TEST_WORKFLOW_TEMPLATE_INTERNAL_NAME,
            'label': TEST_WORKFLOW_TEMPLATE_LABEL,
        }

        if extra_data:
            data.update(extra_data)

        pk_list = list(Workflow.objects.values('pk'))

        response = self.post(
            viewname='rest_api:workflow-template-list', data=data
        )

        try:
            self.test_workflow_template = Workflow.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Workflow.DoesNotExist:
            self.test_workflow_template = None

        return response

    def _request_test_workflow_template_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-detail', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-detail', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-detail', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }, data={'label': TEST_WORKFLOW_TEMPLATE_LABEL_EDITED}
        )

    def _request_test_workflow_template_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:workflow-template-detail', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }, data={
                'internal_name': TEST_WORKFLOW_TEMPLATE_INTERNAL_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_LABEL_EDITED
            }
        )

    def _request_test_workflow_template_image_view_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-image', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_list_api_view(self):
        return self.get(viewname='rest_api:workflow-template-list')


class WorkflowInstanceViewTestMixin:
    def _request_test_document_workflow_instance_list_view(self):
        return self.get(
            viewname='document_states:workflow_instance_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_workflow_instance_detail_view(self):
        return self.get(
            viewname='document_states:workflow_instance_detail',
            kwargs={
                'workflow_instance_id': self.test_workflow_instance.pk
            }
        )

    def _request_test_workflow_instance_transition_execute_view(self):
        return self.post(
            viewname='document_states:workflow_instance_transition_execute',
            kwargs={
                'workflow_instance_id': self.test_workflow_instance.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk,
            }
        )

    def _request_test_workflow_instance_transition_selection_get_view(self):
        return self.get(
            viewname='document_states:workflow_instance_transition_selection',
            kwargs={
                'workflow_instance_id': self.test_workflow_instance.pk,
            }
        )

    def _request_test_workflow_instance_transition_selection_post_view(self):
        return self.post(
            viewname='document_states:workflow_instance_transition_selection',
            kwargs={
                'workflow_instance_id': self.test_workflow_instance.pk,
            }, data={
                'transition': self.test_workflow_template_transition.pk,
            }
        )


class WorkflowTemplateDocumentTypeAPIViewMixin:
    def _request_test_workflow_template_document_type_add_api_view(self):
        return self.post(
            viewname='rest_api:workflow-template-document-type-add',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
            }, data={
                'document_type_id': self.test_document_type.pk
            }
        )

    def _request_test_workflow_template_document_type_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-document-type-list', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_document_type_remove_api_view(self):
        return self.post(
            viewname='rest_api:workflow-template-document-type-remove',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
            }, data={
                'document_type_id': self.test_document_type.pk
            }
        )


class WorkflowRuntimeProxyStateViewTestMixin:
    def _request_test_workflow_runtime_proxy_state_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_state_list',
            kwargs={
                'workflow_runtime_proxy_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_runtime_proxy_state_document_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_state_document_list',
            kwargs={
                'workflow_runtime_proxy_state_id': self.test_workflow_template_states[0].pk
            }
        )


class WorkflowRuntimeProxyViewTestMixin:
    def _request_test_workflow_runtime_proxy_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_list'
        )

    def _request_test_workflow_runtime_proxy_document_list_view(self):
        return self.get(
            viewname='document_states:workflow_runtime_proxy_document_list',
            kwargs={
                'workflow_runtime_proxy_id': self.test_workflow_template.pk
            }
        )


class WorkflowTemplateStateActionTestMixin:
    TestWorkflowAction = TestWorkflowAction
    test_workflow_template_state_action_path = 'mayan.apps.document_states.tests.mixins.TestWorkflowAction'

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

    def _request_test_workflow_state_action_selection_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_action_selection',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }, data={
                'klass': TEST_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH
            }
        )


class WorkflowTemplateStateAPIViewTestMixin:
    def _request_test_workflow_state_create_api_view(self):
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

    def _request_test_workflow_state_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_state_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }
        )

    def _request_test_workflow_state_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-state-list', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_state_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-state-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_state_id': self.test_workflow_template_state.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
            }
        )

    def _request_test_workflow_state_edit_put_api_view(self):
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
    def _request_test_workflow_state_create_view(self, extra_data=None):
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

    def _request_test_workflow_state_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_delete',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_states[0].pk
            }
        )

    def _request_test_workflow_state_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_state_edit',
            kwargs={
                'workflow_template_state_id': self.test_workflow_template_states[0].pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
            }
        )

    def _request_test_workflow_state_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_state_list',
            kwargs={'workflow_template_id': self.test_workflow_template.pk}
        )


class WorkflowTemplateTestMixin:
    def setUp(self):
        super().setUp()
        self.test_workflow_runtime_proxies = []
        self.test_workflow_template_state_runtime_proxies = []
        self.test_workflow_template_states = []
        self.test_workflow_template_transitions = []
        self.test_workflow_templates = []

    def _create_test_workflow_template(
        self, add_test_document_type=False, auto_launch=True
    ):
        total_test_workflow_templates = len(self.test_workflow_templates)
        label = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_LABEL, total_test_workflow_templates
        )
        internal_name = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_INTERNAL_NAME,
            total_test_workflow_templates
        )

        self.test_workflow_template = Workflow.objects.create(
            auto_launch=auto_launch, label=label,
            internal_name=internal_name
        )
        self.test_workflow_templates.append(
            self.test_workflow_template
        )
        self.test_workflow_runtime_proxy = WorkflowRuntimeProxy.objects.get(
            pk=self.test_workflow_template.pk
        )
        self.test_workflow_runtime_proxies.append(
            self.test_workflow_runtime_proxy
        )

        if add_test_document_type:
            self.test_workflow_template.document_types.add(
                self.test_document_type
            )

    def _create_test_workflow_template_state(self):
        total_test_workflow_template_states = len(
            self.test_workflow_template_states
        )
        label = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_STATE_LABEL,
            total_test_workflow_template_states
        )
        initial = total_test_workflow_template_states == 0

        self.test_workflow_template_state = self.test_workflow_template.states.create(
            completion=TEST_WORKFLOW_TEMPLATE_STATE_COMPLETION, initial=initial,
            label=label
        )
        self.test_workflow_template_states.append(
            self.test_workflow_template_state
        )
        self.test_workflow_template_state_runtime_proxy = WorkflowStateRuntimeProxy.objects.get(
            pk=self.test_workflow_template_state.pk
        )
        self.test_workflow_template_state_runtime_proxies.append(
            self.test_workflow_template_state_runtime_proxy
        )

    def _create_test_workflow_template_transition(self):
        total_test_workflow_template_transitions = len(
            self.test_workflow_template_transitions
        )
        label = '{}_{}'.format(
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
            total_test_workflow_template_transitions
        )

        self.test_workflow_template_transition = self.test_workflow_template.transitions.create(
            label=label,
            origin_state=self.test_workflow_template_states[0],
            destination_state=self.test_workflow_template_states[1],
        )

        self.test_workflow_template_transitions.append(
            self.test_workflow_template_transition
        )

    def _create_test_workflow_template_instance_log_entry(self):
        self.test_document.workflows.first().log_entries.create(
            comment=TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT,
            transition=self.test_workflow_template_transition,
            user=self._test_case_user
        )

    def _transition_test_workflow_instance(self, extra_data=None):
        self.test_document.workflows.first().do_transition(
            comment=TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT,
            extra_data=extra_data,
            transition=self.test_workflow_template_transition
        )


class WorkflowToolViewTestMixin:
    def _request_workflow_launch_view(self):
        return self.post(
            viewname='document_states:tool_launch_workflows',
        )


class WorkflowTransitionEventViewTestMixin:
    def _request_test_workflow_template_transition_event_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_events',
            kwargs={
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }
        )


class WorkflowTransitionFieldViewTestMixin:
    def _request_workflow_template_transition_field_create_view(self):
        pk_list = list(
            WorkflowTransitionField.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='document_states:workflow_template_transition_field_create',
            kwargs={
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }, data={
                'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
                'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
            }
        )

        try:
            self.test_workflow_template_transition_field = WorkflowTransitionField.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransitionField.DoesNotExist:
            self.test_workflow_template_transition_field = None

        return response

    def _request_workflow_template_transition_field_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_field_delete',
            kwargs={
                'workflow_template_transition_field_id': self.test_workflow_template_transition_field.pk
            },
        )

    def _request_workflow_template_transition_field_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_field_edit',
            kwargs={
                'workflow_template_transition_field_id': self.test_workflow_template_transition_field.pk
            }, data={
                'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL_EDITED,
                'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
            }
        )

    def _request_test_workflow_template_transition_field_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_field_list',
            kwargs={
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }
        )


class WorkflowTemplateTransitionAPIViewTestMixin:
    def _request_test_workflow_template_transition_create_api_view(
        self, extra_data=None
    ):
        data = {
            'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
            'origin_state_id': self.test_workflow_template_states[0].pk,
            'destination_state_id': self.test_workflow_template_states[1].pk,
        }

        if extra_data:
            data.update(extra_data)

        pk_list = list(
            WorkflowTransition.objects.values_list('pk', flat=True)
        )

        response = self.post(
            viewname='rest_api:workflow-template-transition-list', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }, data=data
        )

        try:
            self.test_workflow_template_transition = WorkflowTransition.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransition.DoesNotExist:
            self.test_workflow_template_transition = None

        return response

    def _request_test_workflow_template_transition_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-list',
            kwargs={'workflow_template_id': self.test_workflow_template.pk}
        )

    def _request_test_workflow_template_transition_edit_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
                'origin_state_id': self.test_workflow_template_states[1].pk,
                'destination_state_id': self.test_workflow_template_states[0].pk,
            }
        )

    def _request_test_workflow_template_transition_edit_put_api_view_via(self):
        return self.put(
            viewname='rest_api:workflow-template-transition-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
                'origin_state_id': self.test_workflow_template_states[1].pk,
                'destination_state_id': self.test_workflow_template_states[0].pk,
            }
        )


class WorkflowTransitionFieldAPIViewTestMixin:
    def _request_test_workflow_template_transition_field_create_api_view(self):
        pk_list = list(WorkflowTransitionField.objects.values_list('pk'))

        response = self.post(
            viewname='rest_api:workflow-template-transition-field-list',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk,
            }, data={
                'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
                'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
            }
        )

        try:
            self.test_workflow_template_transition_field = WorkflowTransitionField.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransitionField.DoesNotExist:
            self.test_workflow_template_transition_field = None

        return response

    def _request_test_workflow_template_transition_field_delete_api_view(self):
        return self.delete(
            viewname='rest_api:workflow-template-transition-field-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk,
                'workflow_template_transition_field_id': self.test_workflow_template_transition_field.pk,
            }
        )

    def _request_test_workflow_template_transition_field_detail_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-field-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk,
                'workflow_template_transition_field_id': self.test_workflow_template_transition_field.pk,
            }
        )

    def _request_test_workflow_template_transition_field_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:workflow-template-transition-field-detail',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk,
                'workflow_template_transition_field_id': self.test_workflow_template_transition_field.pk,
            }, data={
                'label': '{} edited'.format(
                    self.test_workflow_template_transition_field
                )
            }
        )

    def _request_test_workflow_template_transition_field_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-template-transition-field-list',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
                'workflow_template_transition_id': self.test_workflow_template_transition.pk,
            }
        )


class WorkflowTransitionFieldTestMixin:
    def _create_test_workflow_template_transition_field(self, extra_data=None):
        kwargs = {
            'field_type': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_TYPE,
            'name': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_NAME,
            'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_LABEL,
            'help_text': TEST_WORKFLOW_TEMPLATE_TRANSITION_FIELD_HELP_TEXT
        }
        kwargs.update(extra_data or {})

        self.test_workflow_template_transition_field = self.test_workflow_template_transition.fields.create(
            **kwargs
        )


class WorkflowTransitionViewTestMixin:
    def _request_test_workflow_template_transition_create_view(self):
        pk_list = list(WorkflowTransition.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='document_states:workflow_template_transition_create',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL,
                'origin_state': self.test_workflow_template_states[0].pk,
                'destination_state': self.test_workflow_template_states[1].pk,
            }
        )

        try:
            self.test_workflow_template_transition = WorkflowTransition.objects.get(
                ~Q(pk__in=pk_list)
            )
        except WorkflowTransition.DoesNotExist:
            self.test_workflow_template_transition = None

        return response

    def _request_test_workflow_template_transition_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_delete',
            kwargs={
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }
        )

    def _request_test_workflow_template_transition_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_edit',
            kwargs={
                'workflow_template_transition_id': self.test_workflow_template_transition.pk
            }, data={
                'label': TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED,
                'origin_state': self.test_workflow_template_states[0].pk,
                'destination_state': self.test_workflow_template_states[1].pk,
            }
        )

    def _request_test_workflow_template_transition_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_list',
            kwargs={'workflow_template_id': self.test_workflow_template.pk}
        )


class WorkflowTemplateViewTestMixin:
    def _request_test_workflow_template_create_view(self):
        data = {
            'internal_name': TEST_WORKFLOW_TEMPLATE_INTERNAL_NAME,
            'label': TEST_WORKFLOW_TEMPLATE_LABEL,
        }

        pk_list = list(Workflow.objects.values('pk'))

        response = self.post(
            viewname='document_states:workflow_template_create', data=data
        )

        try:
            self.test_workflow_template = Workflow.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Workflow.DoesNotExist:
            self.test_workflow_template = None

        return response

    def _request_test_workflow_template_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_single_delete',
            kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_edit_view(self):
        return self.post(
            viewname='document_states:workflow_template_edit', kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
            }, data={
                'auto_launch': True,
                'label': TEST_WORKFLOW_TEMPLATE_LABEL_EDITED,
                'internal_name': self.test_workflow_template.internal_name
            }
        )

    def _request_test_workflow_template_launch_view(self):
        return self.post(
            viewname='document_states:workflow_template_launch', kwargs={
                'workflow_template_id': self.test_workflow_template.pk
            }
        )

    def _request_test_workflow_template_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_list',
        )

    def _request_test_workflow_template_preview_view(self):
        return self.get(
            viewname='document_states:workflow_template_preview', kwargs={
                'workflow_template_id': self.test_workflow_template.pk,
            }
        )
