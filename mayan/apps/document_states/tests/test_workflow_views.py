from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_workflow_template_created, event_workflow_template_edited
)
from ..models import Workflow
from ..permissions import (
    permission_workflow_template_create, permission_workflow_template_delete,
    permission_workflow_template_edit, permission_workflow_template_view,
    permission_workflow_tools
)

from .literals import TEST_WORKFLOW_TEMPLATE_LABEL
from .mixins.workflow_instance_mixins import DocumentWorkflowTemplateViewTestMixin
from .mixins.workflow_template_mixins import (
    DocumentTypeAddRemoveWorkflowTemplateViewTestMixin,
    WorkflowTemplateDocumentTypeViewTestMixin, WorkflowTemplateTestMixin,
    WorkflowTemplateViewTestMixin, WorkflowToolViewTestMixin
)


class DocumentTypeAddRemoveWorkflowTemplateViewTestCase(
    DocumentTypeAddRemoveWorkflowTemplateViewTestMixin,
    WorkflowTemplateTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()

    def test_document_type_workflow_template_add_remove_get_view_no_permission(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_workflow_template),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_remove_get_view_with_document_type_access(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self.test_workflow_template),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_remove_get_view_with_workflow_template_access(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_workflow_template),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_remove_get_view_with_full_access(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_workflow_template),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template not in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_workflow_template not in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_view_with_workflow_template_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template not in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_add_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_workflow_template in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_document_type_workflow_template_remove_view_no_permission(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_remove_view_with_document_type_access(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self.test_workflow_template in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_remove_view_with_workflow_template_access(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_workflow_template_remove_view_with_full_access(self):
        self.test_document_type.workflows.add(
            self.test_workflow_template
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_document_type_workflow_template_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_workflow_template not in self.test_document_type.workflows.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)


class DocumentWorkflowTemplateViewTestCase(
    DocumentWorkflowTemplateViewTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )
        self.test_workflow_template.auto_launch = False
        self.test_workflow_template.save()

    def test_document_single_workflow_launch_view_no_permission(self):
        self._create_test_document_stub()

        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_test_document_single_workflow_template_launch_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_single_workflow_launch_view_with_document_access(self):
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_document, permission=permission_workflow_tools
        )

        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_test_document_single_workflow_template_launch_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_single_workflow_launch_view_with_workflow_access(self):
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_tools
        )

        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_test_document_single_workflow_template_launch_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_single_workflow_launch_view_with_full_access(self):
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_document, permission=permission_workflow_tools
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_tools
        )

        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_test_document_single_workflow_template_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_single_workflow_launch_view_with_full_access(self):
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_document, permission=permission_workflow_tools
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_tools
        )

        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_single_workflow_template_launch_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowTemplateDocumentTypeViewTestCase(
    WorkflowTemplateDocumentTypeViewTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()

    def test_workflow_template_document_type_add_remove_get_view_no_permission(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_workflow_template),
            status_code=404
        )

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_remove_get_view_with_document_type_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self.test_workflow_template),
            status_code=404
        )

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_remove_get_view_with_workflow_template_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_workflow_template),
            status_code=200
        )

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_remove_get_view_with_full_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self.test_document_type),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self.test_workflow_template),
            status_code=200
        )

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_view_no_permission(self):
        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_view_with_document_type_access(self):
        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_view_with_workflow_template_access(self):
        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_view_with_full_access(self):
        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_document_type_remove_view_no_permission(self):
        self.test_workflow_template.document_types.add(self.test_document_type)

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_view_with_document_type_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_view_with_workflow_template_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_view_with_full_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        test_workflow_template_document_type_count = self.test_workflow_template.document_types.count()

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_type_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)


class WorkflowTemplateViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin,
    GenericViewTestCase
):
    def test_workflow_template_create_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Workflow.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_create_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_template_create)

        self._clear_events()

        response = self._request_test_workflow_template_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Workflow.objects.count(), 1)
        self.assertEqual(
            Workflow.objects.all()[0].label, TEST_WORKFLOW_TEMPLATE_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_created.id)

    def test_workflow_template_delete_view_no_permission(self):
        self._create_test_workflow_template()

        self._clear_events()

        response = self._request_test_workflow_template_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template in Workflow.objects.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_delete_view_with_access(self):
        self._create_test_workflow_template()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_delete
        )

        self._clear_events()

        response = self._request_test_workflow_template_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.test_workflow_template in Workflow.objects.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_edit_view_no_permission(self):
        self._create_test_workflow_template()

        test_workflow_template_label = self.test_workflow_template.label

        self._clear_events()

        response = self._request_test_workflow_template_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template.label, test_workflow_template_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_edit_view_with_access(self):
        self._create_test_workflow_template()

        test_workflow_template_label = self.test_workflow_template.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_template.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template.label, test_workflow_template_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_list_view_no_permission(self):
        self._create_test_workflow_template()

        self._clear_events()

        response = self._request_test_workflow_template_list_view()

        self.assertNotContains(
            response=response, text=self.test_workflow_template.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_list_view_with_access(self):
        self._create_test_workflow_template()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_template.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_preview_view_no_permission(self):
        self._create_test_workflow_template()

        self._clear_events()

        response = self._request_test_workflow_template_preview_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self.test_workflow_template in Workflow.objects.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_preview_view_with_access(self):
        self._create_test_workflow_template()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_preview_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowTemplateDocumentViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTemplateViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflows_launch_view_no_permission(self):
        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_test_workflow_template_launch_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflows_launch_view_with_permission(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_tools
        )

        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_test_workflow_template_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_workflows_launch_view_with_permission(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_tools
        )

        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_workflow_template_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class WorkflowToolViewTestCase(
    WorkflowTemplateTestMixin, WorkflowToolViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_tool_launch_workflows_view_no_permission(self):
        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tool_launch_workflows_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_tools)

        workflow_instance_count = self.test_document.workflows.count()

        self._clear_events()

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_tool_launch_workflows_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_tools)

        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
