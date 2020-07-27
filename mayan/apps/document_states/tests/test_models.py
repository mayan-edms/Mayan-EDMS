import json

from mayan.apps.documents.events import event_document_properties_edit
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.events.classes import EventType
from mayan.apps.tests.tests.base import BaseTestCase

from .literals import (
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_DOTTED_PATH,
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_LABEL,
    TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DESCRIPTION,
    TEST_WORKFLOW_STATE_ACTION_LABEL,
    TEST_WORKFLOW_STATE_ACTION_LABEL_2
)
from .mixins import WorkflowStateActionTestMixin, WorkflowTestMixin


class WorkflowInstanceModelTestCase(
    WorkflowTestMixin, GenericDocumentTestCase
):
    auto_upload_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self.test_workflow.document_types.add(self.test_document_type)

    def test_workflow_method_get_absolute_url(self):
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_instance.get_absolute_url()

    def test_workflow_no_auto_launche(self):
        self.test_workflow.auto_launch = False
        self.test_workflow.save()

        self._upload_test_document()
        self.assertEqual(self.test_document.workflows.count(), 0)

    def test_workflow_transition_no_condition(self):
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()
        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 1
        )

    def test_workflow_transition_false_condition(self):
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_transition.condition = '{{ invalid_variable }}'
        self.test_workflow_transition.save()

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 0
        )

    def test_workflow_transition_true_condition(self):
        self._upload_test_document()
        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_transition.condition = '{{ workflow_instance }}'
        self.test_workflow_transition.save()

        self.assertEqual(
            self.test_workflow_instance.get_transition_choices().count(), 1
        )


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
        self.test_workflow.document_types.add(self.test_document_type)

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

    def test_workflow_state_action_event_trigger(self):
        # actions 1 and 2 both trigger the transition event, to make this
        # test case independent of the order of execution of actions 1 and 2
        state_1_action_data = json.dumps(obj={
            'document_label': TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_LABEL
        })
        self.test_workflow_state_1.actions.create(
            label=TEST_WORKFLOW_STATE_ACTION_LABEL,
            action_path=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_DOTTED_PATH,
            action_data=state_1_action_data
        )
        self.test_workflow_state_1.actions.create(
            label=TEST_WORKFLOW_STATE_ACTION_LABEL_2,
            action_path=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_DOTTED_PATH,
            action_data=state_1_action_data
        )

        state_2_action_data = json.dumps(obj={
            'document_description': TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DESCRIPTION
        })
        self.test_workflow_state_2.actions.create(
            label=TEST_WORKFLOW_STATE_ACTION_LABEL,
            action_path=TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_DOTTED_PATH,
            action_data=state_2_action_data
        )

        EventType.refresh()

        self.test_workflow_transition.trigger_events.create(
            event_type=event_document_properties_edit.get_stored_event_type()
        )

        self.test_workflow.launch_for(
            document=self.test_document
        )

        self.assertEqual(
            self.test_document.label,
            TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_LABEL
        )
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_EDIT_WORKFLOW_ACTION_TEXT_DESCRIPTION
        )
