from __future__ import unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..literals import FIELD_TYPE_CHOICE_CHAR
from ..models import WorkflowTransition
from ..permissions import (
    permission_workflow_edit, permission_workflow_view,
    permission_workflow_transition
)

from .literals import (
    TEST_WORKFLOW_TRANSITION_FIELD_HELP_TEXT,
    TEST_WORKFLOW_TRANSITION_FIELD_LABEL, TEST_WORKFLOW_TRANSITION_FIELD_NAME,
    TEST_WORKFLOW_TRANSITION_FIELD_TYPE, TEST_WORKFLOW_TRANSITION_LABEL,
    TEST_WORKFLOW_TRANSITION_LABEL_EDITED
)
from .mixins import (
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowTransitionViewTestMixin
)

TEST_WORKFLOW_TRANSITION_FIELD_NAME = 'test_workflow_transition_field'
TEST_WORKFLOW_TRANSITION_FIELD_LABEL = 'test workflow transition field'
TEST_WORKFLOW_TRANSITION_FIELD_HELP_TEXT = 'test workflow transition field help test'
TEST_WORKFLOW_TRANSITION_FIELD_TYPE = FIELD_TYPE_CHOICE_CHAR


class WorkflowTransitionViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericViewTestCase
):
    def test_create_test_workflow_transition_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        response = self._request_test_workflow_transition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowTransition.objects.count(), 0)

    def test_create_test_workflow_transition_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowTransition.objects.count(), 1)
        self.assertEqual(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TRANSITION_LABEL
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].origin_state,
            self.test_workflow_state_1
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].destination_state,
            self.test_workflow_state_2
        )

    def test_delete_workflow_transition_no_permissions(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )

    def test_delete_workflow_transition_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(permission=permission_workflow_edit, obj=self.test_workflow)

        response = self._request_test_workflow_transition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_workflow_transition in WorkflowTransition.objects.all()
        )

    def test_edit_workflow_transition_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label, TEST_WORKFLOW_TRANSITION_LABEL
        )

    def test_edit_workflow_transition_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_transition.label,
            TEST_WORKFLOW_TRANSITION_LABEL_EDITED
        )

    def test_workflow_transition_list_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=404
        )

    def test_workflow_transition_list_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_transition_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_transition.label,
            status_code=200
        )


class WorkflowTransitionDocumentViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_document = False

    def setUp(self):
        super(WorkflowTransitionDocumentViewTestCase, self).setUp()
        self._create_test_workflow()
        self.test_workflow.document_types.add(self.test_document_type)
        self._create_test_workflow_states()
        self._create_test_workflow_transitions()
        self.upload_document()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_transition_workflow_no_access(self):
        """
        Test transitioning a workflow without the transition workflow
        permission.
        """
        response = self._request_test_workflow_transition()
        self.assertEqual(response.status_code, 404)

        # Workflow should remain in the same initial state
        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_1
        )

    def test_transition_workflow_with_workflow_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_transition
        )

        response = self._request_test_workflow_transition()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )

    def test_transition_workflow_with_transition_access(self):
        """
        Test transitioning a workflow by granting the transition workflow
        permission to the role.
        """
        self.grant_access(
            obj=self.test_workflow_transition,
            permission=permission_workflow_transition
        )

        response = self._request_test_workflow_transition()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_instance.get_current_state(),
            self.test_workflow_state_2
        )


class WorkflowTransitionEventViewTestCase(
    WorkflowTestMixin, GenericDocumentViewTestCase
):
    def _request_test_workflow_transition_event_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_events',
            kwargs={'pk': self.test_workflow_transition.pk}
        )

    def test_workflow_transition_event_list_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_transition_event_list_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_event_list_view()
        self.assertEqual(response.status_code, 200)


class WorkflowTransitionFieldViewTestCase(
    WorkflowTestMixin, WorkflowTransitionViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super(WorkflowTransitionFieldViewTestCase, self).setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

    def _create_test_workflow_transition_field(self):
        self.test_workflow_transition_field = self.test_workflow_transition.fields.create(
            field_type=TEST_WORKFLOW_TRANSITION_FIELD_TYPE,
            name=TEST_WORKFLOW_TRANSITION_FIELD_NAME,
            label=TEST_WORKFLOW_TRANSITION_FIELD_LABEL,
            help_text=TEST_WORKFLOW_TRANSITION_FIELD_HELP_TEXT
        )

    def _request_test_workflow_transition_field_list_view(self):
        return self.get(
            viewname='document_states:workflow_template_transition_field_list',
            kwargs={'pk': self.test_workflow_transition.pk}
        )

    def test_workflow_transition_field_list_view_no_permission(self):
        self._create_test_workflow_transition_field()

        response = self._request_test_workflow_transition_field_list_view()
        self.assertNotContains(
            response=response,
            text=self.test_workflow_transition_field.label,
            status_code=404
        )

    def test_workflow_transition_field_list_view_with_access(self):
        self._create_test_workflow_transition_field()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_transition_field_list_view()
        self.assertContains(
            response=response,
            text=self.test_workflow_transition_field.label,
            status_code=200
        )

    def _request_workflow_transition_field_create_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_field_create',
            kwargs={'pk': self.test_workflow_transition.pk},
            data={
                'field_type': TEST_WORKFLOW_TRANSITION_FIELD_TYPE,
                'name': TEST_WORKFLOW_TRANSITION_FIELD_NAME,
                'label': TEST_WORKFLOW_TRANSITION_FIELD_LABEL,
                'help_text': TEST_WORKFLOW_TRANSITION_FIELD_HELP_TEXT
            }
        )

    def test_workflow_transition_field_create_view_no_permission(self):
        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        response = self._request_workflow_transition_field_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count
        )

    def test_workflow_transition_field_create_view_with_access(self):
        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_workflow_transition_field_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count + 1
        )

    def _request_workflow_transition_field_delete_view(self):
        return self.post(
            viewname='document_states:workflow_template_transition_field_delete',
            kwargs={'pk': self.test_workflow_transition_field.pk},
        )

    def test_workflow_transition_field_delete_view_no_permission(self):
        self._create_test_workflow_transition_field()

        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        response = self._request_workflow_transition_field_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count
        )

    def test_workflow_transition_field_delete_view_with_access(self):
        self._create_test_workflow_transition_field()

        workflow_transition_field_count = self.test_workflow_transition.fields.count()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_workflow_transition_field_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_transition.fields.count(),
            workflow_transition_field_count - 1
        )
