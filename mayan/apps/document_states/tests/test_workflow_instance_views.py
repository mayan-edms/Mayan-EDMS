from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..literals import WIDGET_CLASS_TEXTAREA
from ..permissions import (
    permission_workflow_transition, permission_workflow_view
)

from .mixins import (
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowInstanceViewTestMixin,
    WorkflowTransitionFieldTestMixin
)


class WorkflowInstanceTransitionViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowInstanceViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_document_workflow_instance_list_view_no_permission(self):
        response = self._request_test_document_workflow_instance_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_workflow_instance_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_workflow_view
        )

        response = self._request_test_document_workflow_instance_list_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
        )

    def test_trashed_document_workflow_instance_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_workflow_view
        )

        self.test_document.delete()

        response = self._request_test_document_workflow_instance_list_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_instance_detail_view_no_permission(self):
        response = self._request_test_workflow_instance_detail_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_instance_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_workflow_view
        )

        response = self._request_test_workflow_instance_detail_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
        )

    def test_trashed_document_workflow_instance_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_workflow_view
        )

        self.test_document.delete()

        response = self._request_test_workflow_instance_detail_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_instance_transition_selection_get_view_no_permission(self):
        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_workflow_instance_transition_selection_get_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )
        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_trashed_document_workflow_instance_transition_selection_get_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        self.test_document.delete()

        response = self._request_test_workflow_instance_transition_selection_get_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_instance_transition_selection_post_view_no_permission(self):
        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_workflow_instance_transition_selection_post_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )
        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_trashed_document_workflow_instance_transition_selection_post_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        self.test_document.delete()

        response = self._request_test_workflow_instance_transition_selection_post_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_instance_transition_execute_view_no_permission(self):
        """
        Test transitioning a workflow without the transition workflow
        permission.
        """
        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

        # Workflow should remain in the same initial state
        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_workflow_instance_transition_execute_view_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

    def test_workflow_instance_transition_execute_view_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

    def test_trashed_document_workflow_instance_transition_execute_view_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        self.test_document.delete()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)

    def test_trashed_document_workflow_instance_transition_execute_view_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        self.test_document.delete()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)


class WorkflowInstanceTransitionFieldViewTestCase(
    WorkflowTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowInstanceViewTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._create_test_workflow_transition_field(
            extra_data={
                'widget': WIDGET_CLASS_TEXTAREA
            }
        )
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_workflow_instance_transition_text_area_widget_execute_view_with_transition_access(self):
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

    def test_trashed_document_workflow_transition_text_area_widget_execute_view_with_transition_access(self):
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        self.test_document.delete()

        response = self._request_test_workflow_instance_transition_execute_view()
        self.assertEqual(response.status_code, 404)
