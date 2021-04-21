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
