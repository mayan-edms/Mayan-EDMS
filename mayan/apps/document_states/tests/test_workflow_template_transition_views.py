from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_template_edited
from ..models import WorkflowTransition
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .literals import TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
from .mixins.workflow_instance_mixins import WorkflowInstanceViewTestMixin
from .mixins.workflow_template_mixins import (
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin
)
from .mixins.workflow_template_transition_mixins import (
    WorkflowTransitionEventViewTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTransitionViewTestMixin
)


class WorkflowTransitionViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin,
    WorkflowTransitionViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()

    def test_workflow_template_transition_create_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_transition_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowTransition.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_create_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowTransition.objects.count(), 1)
        self.assertEqual(
            WorkflowTransition.objects.all()[0].label,
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].origin_state,
            self.test_workflow_template_states[0]
        )
        self.assertEqual(
            WorkflowTransition.objects.all()[0].destination_state,
            self.test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_workflow_template_transition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_delete_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template_transition in WorkflowTransition.objects.all()
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_delete_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_workflow_template_transition in WorkflowTransition.objects.all()
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_edit_view_no_permission(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self.test_workflow_template_transition.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_view_with_access(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self.test_workflow_template_transition.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_workflow_template_transition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_list_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_view()
        self.assertNotContains(
            response=response,
            text=self.test_workflow_template_transition.label,
            status_code=404
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_list_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_view()
        self.assertContains(
            response=response,
            text=self.test_workflow_template_transition.label,
            status_code=200
        )
        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowTransitionEventViewTestCase(
    WorkflowInstanceViewTestMixin, WorkflowTemplateTestMixin,
    WorkflowTransitionEventViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()
        self.test_workflow_instance = self.test_document.workflows.first()

    def test_workflow_template_transition_event_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_transition_event_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_event_list_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_event_list_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowTransitionFieldViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTransitionFieldTestMixin,
    WorkflowTransitionFieldViewTestMixin, WorkflowTransitionViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_template_transition_field_create_view_no_permission(self):
        workflow_template_transition_field_count = self.test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_workflow_template_transition_field_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_create_view_with_access(self):
        workflow_template_transition_field_count = self.test_workflow_template_transition.fields.count()
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_workflow_template_transition_field_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self.test_workflow_template_transition_field
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_delete_view_no_permission(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_count = self.test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_workflow_template_transition_field_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_delete_view_with_access(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_count = self.test_workflow_template_transition.fields.count()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_workflow_template_transition_field_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            workflow_template_transition_field_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_edit_view_no_permission(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_label = self.test_workflow_template_transition_field.label

        self._clear_events()

        response = self._request_workflow_template_transition_field_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_template_transition_field.refresh_from_db()
        self.assertEqual(
            workflow_template_transition_field_label,
            self.test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_edit_view_with_access(self):
        self._create_test_workflow_template_transition_field()
        workflow_template_transition_field_label = self.test_workflow_template_transition_field.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_workflow_template_transition_field_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_template_transition_field.refresh_from_db()
        self.assertNotEqual(
            workflow_template_transition_field_label,
            self.test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object,
            self.test_workflow_template_transition_field
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_list_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_view()
        self.assertNotContains(
            response=response,
            text=self.test_workflow_template_transition_field.label,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_list_view_with_access(self):
        self._create_test_workflow_template_transition_field()
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_view()
        self.assertContains(
            response=response,
            text=self.test_workflow_template_transition_field.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
