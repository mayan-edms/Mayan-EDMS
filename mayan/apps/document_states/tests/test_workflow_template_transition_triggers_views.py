from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_workflow_template_view

from .mixins.workflow_instance_mixins import WorkflowInstanceViewTestMixin
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import (
    WorkflowTemplateTransitionTriggerViewTestMixin
)


class WorkflowTransitionTriggerViewTestCase(
    WorkflowInstanceViewTestMixin, WorkflowTemplateTestMixin,
    WorkflowTemplateTransitionTriggerViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition()

    def test_workflow_template_transition_trigger_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_transition_event_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_list_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_event_list_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
