from django.db.models import Q

from ...models import (
    Workflow, WorkflowRuntimeProxy, WorkflowStateRuntimeProxy
)
from ...tasks import (
    task_launch_all_workflows, task_launch_all_workflow_for,
    task_launch_workflow, task_launch_workflow_for
)

from ..literals import (
    TEST_WORKFLOW_INSTANCE_LOG_ENTRY_COMMENT,
    TEST_WORKFLOW_TEMPLATE_INTERNAL_NAME, TEST_WORKFLOW_TEMPLATE_LABEL,
    TEST_WORKFLOW_TEMPLATE_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_COMPLETION,
    TEST_WORKFLOW_TEMPLATE_STATE_LABEL,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
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


class WorkflowTaskTestCaseMixin:
    def _execute_task_launch_all_workflows(self):
        task_launch_all_workflows.apply_async().get()

    def _execute_task_launch_all_workflow_for(self):
        task_launch_all_workflow_for.apply_async(
            kwargs={
                'document_id': self.test_document.pk,
            }
        ).get()

    def _execute_task_launch_workflow(self):
        task_launch_workflow.apply_async(
            kwargs={
                'workflow_id': self.test_workflow_template.pk
            }
        ).get()

    def _execute_task_launch_workflow_for(self):
        task_launch_workflow_for.apply_async(
            kwargs={
                'document_id': self.test_document.pk,
                'workflow_id': self.test_workflow_template.pk
            }
        ).get()


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
        initial = self.test_workflow_template.states.count() == 0

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
