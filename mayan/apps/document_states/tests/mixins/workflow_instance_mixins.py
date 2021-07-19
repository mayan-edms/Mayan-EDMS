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


class WorkflowInstanceLogEntryTransitrionListAPIViewTestMixin:
    def _request_test_workflow_instance_log_entry_transition_list_api_view(self):
        return self.get(
            viewname='rest_api:workflow-instance-log-entry-transition-list',
            kwargs={
                'document_id': self.test_document.pk,
                'workflow_instance_id': self.test_workflow_instance.pk
            }
        )


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


class WorkflowToolViewTestMixin:
    def _request_workflow_launch_view(self):
        return self.post(
            viewname='document_states:tool_launch_workflows',
        )
