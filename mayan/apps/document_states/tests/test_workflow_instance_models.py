from mayan.apps.documents.events import event_document_type_changed
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class WorkflowInstanceModelTestCase(
    WorkflowTemplateTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self.test_workflow_template.document_types.add(self.test_document_type)

    def test_workflow_launch_on_document_type_change(self):
        self._create_test_document_type()

        self._create_test_document_stub()

        self._clear_events()

        self.assertEqual(self.test_document.workflows.count(), 0)

        self.test_document.document_type_change(
            document_type=self.test_document_types[0],
            _user=self._test_case_user
        )

        self.assertEqual(self.test_document.workflows.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_types[0])
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_type_changed.id)

    def test_workflow_instance_method_get_absolute_url(self):
        self._create_test_document_stub()

        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_instance.get_absolute_url()

    def test_workflow_template_auto_launch(self):
        self.test_workflow_template.auto_launch = True
        self.test_workflow_template.save()

        self._create_test_document_stub()

        self.assertEqual(self.test_document.workflows.count(), 1)

    def test_workflow_template_no_auto_launch(self):
        self.test_workflow_template.auto_launch = False
        self.test_workflow_template.save()

        self._create_test_document_stub()

        self.assertEqual(self.test_document.workflows.count(), 0)

    def test_workflow_template_transition_no_condition(self):
        self._create_test_document_stub()

        self.test_workflow_instance = self.test_document.workflows.first()
        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 1
        )

    def test_workflow_template_transition_false_condition(self):
        self._create_test_document_stub()

        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_template_transition.condition = '{{ invalid_variable }}'
        self.test_workflow_template_transition.save()

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 0
        )

    def test_workflow_template_transition_true_condition(self):
        self._create_test_document_stub()

        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_template_transition.condition = '{{ workflow_instance }}'
        self.test_workflow_template_transition.save()

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 1
        )
