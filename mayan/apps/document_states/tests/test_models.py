import json

from mayan.apps.documents.events import event_document_edited
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.events.classes import EventType
from mayan.apps.testing.tests.base import BaseTestCase

from .literals import (
    TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_DOTTED_PATH,
    TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_LABEL,
    TEST_DOCUMENT_EDIT_WORKFLOW_TEMPLATE_STATE_ACTION_TEXT_DESCRIPTION
)
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_state_mixins import WorkflowTemplateStateActionTestMixin
from .mixins.workflow_template_transition_mixins import WorkflowTransitionFieldTestMixin


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

    def test_workflow_method_get_absolute_url(self):
        self._create_test_document_stub()

        self.test_workflow_instance = self.test_document.workflows.first()

        self.test_workflow_instance.get_absolute_url()

    def test_workflow_auto_launch(self):
        self.test_workflow_template.auto_launch = True
        self.test_workflow_template.save()

        self._create_test_document_stub()

        self.assertEqual(self.test_document.workflows.count(), 1)

    def test_workflow_no_auto_launch(self):
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


class WorkflowModelTestCase(WorkflowTemplateTestMixin, BaseTestCase):
    def test_workflow_template_preview(self):
        self._create_test_workflow_template()
        self.assertTrue(self.test_workflow_template.get_api_image_url())


class WorkflowStateActionModelTestCase(
    WorkflowTemplateStateActionTestMixin, WorkflowTemplateTestMixin, GenericDocumentTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self.test_workflow_template.document_types.add(self.test_document_type)

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


class WorkflowTransitionFieldModelTestCase(
    WorkflowTemplateTestMixin,
    WorkflowTransitionFieldTestMixin,
    GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition_field()
        self._create_test_document_stub()

    def test_deleted_field_context_references(self):
        """
        Transition a workflow with a transition field, and the delete the
        transition field. The retrieving the context should work even with an
        obsolete field reference.
        """
        self._transition_test_workflow_instance(
            extra_data={
                self.test_workflow_template_transition_field.name: 'test'
            }
        )
        self.test_document.workflows.first().log_entries.first().get_extra_data()
        self.test_workflow_template_transition_field.delete()
        self.test_document.workflows.first().log_entries.first().get_extra_data()
