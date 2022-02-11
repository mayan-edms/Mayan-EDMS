import json

from mayan.apps.documents.events import event_document_edited
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.events.classes import EventType

from .literals import (
    TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
    TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_LABEL,
    TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_DESCRIPTION
)
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_state_mixins import WorkflowTemplateStateActionTestMixin


class WorkflowTemplateStateActionModelTestCase(
    WorkflowTemplateStateActionTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def _get_test_workflow_state_action_execute_flag(self):
        return getattr(
            self.test_workflow_instance,
            '_workflow_state_action_executed', False
        )

    def test_workflow_initial_state_action_no_condition(self):
        self._create_test_workflow_template_state_action()
        self.test_workflow_instance = self.test_workflow_template.launch_for(
            document=self.test_document
        )
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_initial_state_action_false_condition(self):
        self._create_test_workflow_template_state_action()
        self.test_workflow_template_state_action.condition = '{{ invalid_variable }}'
        self.test_workflow_template_state_action.save()

        self.test_workflow_instance = self.test_workflow_template.launch_for(
            document=self.test_document
        )
        self.assertFalse(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_initial_state_action_true_condition(self):
        self._create_test_workflow_template_state_action()
        self.test_workflow_template_state_action.condition = '{{ workflow_instance }}'
        self.test_workflow_template_state_action.save()

        self.test_workflow_instance = self.test_workflow_template.launch_for(
            document=self.test_document
        )
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_no_condition(self):
        self._create_test_workflow_template_state_action(
            workflow_state_index=1
        )
        self.test_workflow_instance = self.test_workflow_template.launch_for(
            document=self.test_document
        )
        self.test_workflow_instance.do_transition(
            transition=self.test_workflow_template_transition
        )
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_false_condition(self):
        self._create_test_workflow_template_state_action(
            workflow_state_index=1
        )
        self.test_workflow_template_state_action.condition = '{{ invalid_variable }}'
        self.test_workflow_template_state_action.save()

        self.test_workflow_instance = self.test_workflow_template.launch_for(
            document=self.test_document
        )
        self.test_workflow_instance.do_transition(
            transition=self.test_workflow_template_transition
        )
        self.assertFalse(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_true_condition(self):
        self._create_test_workflow_template_state_action(
            workflow_state_index=1
        )
        self.test_workflow_template_state_action.condition = '{{ workflow_instance }}'
        self.test_workflow_template_state_action.save()

        self.test_workflow_instance = self.test_workflow_template.launch_for(
            document=self.test_document
        )
        self.test_workflow_instance.do_transition(
            transition=self.test_workflow_template_transition
        )
        self.assertTrue(self._get_test_workflow_state_action_execute_flag())

    def test_workflow_state_action_event_trigger(self):
        # actions 1 and 2 both trigger the transition event, to make this
        # test case independent of the order of execution of actions 1 and 2
        state_1_action_data = json.dumps(
            obj={
                'document_label': TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_LABEL
            }
        )

        self._create_test_workflow_template_state_action(
            extra_data={
                'action_path': TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
                'action_data': state_1_action_data
            }
        )
        self._create_test_workflow_template_state_action(
            extra_data={
                'action_path': TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
                'action_data': state_1_action_data
            }
        )

        state_2_action_data = json.dumps(
            obj={
                'document_description': TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_DESCRIPTION
            }
        )

        self._create_test_workflow_template_state_action(
            extra_data={
                'action_path': TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
                'action_data': state_2_action_data
            }, workflow_state_index=1
        )

        EventType.refresh()

        self.test_workflow_template_transition.trigger_events.create(
            event_type=event_document_edited.get_stored_event_type()
        )

        self.test_workflow_template.launch_for(
            document=self.test_document
        )

        self.assertEqual(
            self.test_document.label,
            TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_LABEL
        )
        self.assertEqual(
            self.test_document.description,
            TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_DESCRIPTION
        )
