from mayan.apps.tests.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins import WorkflowStateActionTestMixin, WorkflowTestMixin


class WorkflowInstanceModelTestCase(
    WorkflowTestMixin, GenericDocumentTestCase
):
    def test_workflow_transition_no_condition(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 1
        )

    def test_workflow_transition_false_condition(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )

        self.test_workflow_transition.condition = '{{ invalid_variable }}'
        self.test_workflow_transition.save()

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 0
        )

    def test_workflow_transition_true_condition(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )

        self.test_workflow_transition.condition = '{{ workflow_instance }}'
        self.test_workflow_transition.save()

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 1
        )

    def test_workflow_method_get_absolute_url(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )

        self.test_workflow_instance.get_absolute_url()


class WorkflowModelTestCase(WorkflowTestMixin, BaseTestCase):
    def test_workflow_template_preview(self):
        self._create_test_workflow()
        self.assertTrue(self.test_workflow.get_api_image_url())


class WorkflowStateActionModelTestCase(
    WorkflowStateActionTestMixin, WorkflowTestMixin, GenericDocumentTestCase
):
    def setUp(self):
        super(WorkflowStateActionModelTestCase, self).setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

    def _get_test_workflow_state_action_execute_flag(self):
        return getattr(
            self.test_workflow_instance,
            '_workflow_state_action_executed', False
        )

    def test_workflow_initial_state_action_no_condition(self):
        self._create_test_workflow_state_action()
        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_initial_state_action_false_condition(self):
        self._create_test_workflow_state_action()
        self.test_workflow_state_action.condition = '{{ invalid_variable }}'
        self.test_workflow_state_action.save()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )
        self.assertFalse(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_initial_state_action_true_condition(self):
        self._create_test_workflow_state_action()
        self.test_workflow_state_action.condition = '{{ workflow_instance }}'
        self.test_workflow_state_action.save()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_no_condition(self):
        self._create_test_workflow_state_action(workflow_state_index=1)
        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )
        self.test_workflow_instance.do_transition(transition=self.test_workflow_transition)
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_false_condition(self):
        self._create_test_workflow_state_action(workflow_state_index=1)
        self.test_workflow_state_action.condition = '{{ invalid_variable }}'
        self.test_workflow_state_action.save()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )
        self.test_workflow_instance.do_transition(transition=self.test_workflow_transition)
        self.assertFalse(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_true_condition(self):
        self._create_test_workflow_state_action(workflow_state_index=1)
        self.test_workflow_state_action.condition = '{{ workflow_instance }}'
        self.test_workflow_state_action.save()

        self.test_workflow_instance = self.test_workflow.launch_for(
            document=self.test_document
        )
        self.test_workflow_instance.do_transition(transition=self.test_workflow_transition)
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())
