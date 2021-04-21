from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..literals import WIDGET_CLASS_TEXTAREA
from ..permissions import (
    permission_workflow_instance_transition, permission_workflow_template_view
)

from .mixins.workflow_instance_mixins import WorkflowInstanceViewTestMixin
from .mixins.workflow_template_mixins import (
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin
)
from .mixins.workflow_template_transition_mixins import WorkflowTransitionFieldTestMixin


class WorkflowInstanceTransitionViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin,
    WorkflowInstanceViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_document_workflow_instance_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_workflow_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_workflow_instance_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_document_workflow_instance_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_template.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_workflow_instance_list_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_document_workflow_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_workflow_instance_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_template_view
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_document_workflow_instance_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_template.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_instance_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_template_view
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_workflow_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_detail_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_instance_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_detail_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_instance_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_detail_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_instance_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_detail_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_template_view
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_instance_detail_view()
        self.assertContains(
            response=response, text=self.test_workflow_template.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_instance_detail_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_template_view
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_instance_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_get_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_get_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertContains(
            response=response, text=str(self.test_document), status_code=200
        )
        self.assertNotContains(
            response=response,
            text=str(self.test_workflow_template_transitions[0]),
            status_code=200
        )

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_get_view_with_transition_access(self):
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_get_view_with_document_and_transition_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertContains(
            response=response, text=str(self.test_document), status_code=200
        )
        self.assertContains(
            response=response,
            text=str(self.test_workflow_template_transitions[0]),
            status_code=200
        )

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_get_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_get_view_with_document_and_workflow_template_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertContains(
            response=response, text=str(self.test_document), status_code=200
        )
        self.assertContains(
            response=response,
            text=str(self.test_workflow_template_transitions[0]),
            status_code=200
        )

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_instance_transition_selection_get_view_with_document_and_workflow_template_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_post_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_post_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_post_view_with_document_and_transition_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_post_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_selection_post_view_with_document_and_workflow_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_instance_transition_selection_post_view_with_document_and_workflow_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_execute_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_execute_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_execute_view_with_transition_access(self):
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_execute_view_with_document_and_transition_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_execute_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_instance_transition_execute_view_with_document_and_workflow_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_instance_transition_execute_view_with_document_and_workflow_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_instance_transition
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowInstanceTransitionFieldViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowInstanceViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition_field(
            extra_data={
                'widget': WIDGET_CLASS_TEXTAREA
            }
        )
        self._create_test_document_stub()

        self.test_workflow_instance = self.test_document.workflows.first()

    def test_workflow_instance_transition_text_area_widget_execute_view_with_document_and_transition_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflow_instance_transition_text_area_widget_execute_view_with_document_and_transition_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_workflow_instance_transition
        )
        self.grant_access(
            obj=self.test_workflow_template_transition,
            permission=permission_workflow_instance_transition
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
