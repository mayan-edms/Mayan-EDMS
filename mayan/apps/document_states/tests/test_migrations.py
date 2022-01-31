from mayan.apps.testing.tests.base import MayanMigratorTestCase

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class WorkflowTemplateTransitionTriggerMigrationTestCase(
    WorkflowTemplateTestMixin, MayanMigratorTestCase
):
    migrate_from = ('document_states', '0023_auto_20200930_0726')
    migrate_to = (
        'document_states',
        '0024_remove_duplicate_workflow_template_transition_triggers'
    )

    def prepare(self):
        StoredEventType = self.old_state.apps.get_model(
            app_label='events', model_name='StoredEventType'
        )

        Workflow = self.old_state.apps.get_model(
            app_label='document_states', model_name='Workflow'
        )
        WorkflowState = self.old_state.apps.get_model(
            app_label='document_states', model_name='WorkflowState'
        )
        WorkflowTransition = self.old_state.apps.get_model(
            app_label='document_states', model_name='WorkflowTransition'
        )

        WorkflowTransitionTriggerEvent = self.old_state.apps.get_model(
            app_label='document_states',
            model_name='WorkflowTransitionTriggerEvent'
        )

        test_stored_event_type = StoredEventType.objects.create(
            name='test'
        )
        test_workflow_template = Workflow.objects.create(label='test')
        test_workflow_state_0 = WorkflowState.objects.create(
            label='test workflow template state 0',
            workflow=test_workflow_template
        )
        test_workflow_state_1 = WorkflowState.objects.create(
            label='test workflow template state 1',
            workflow=test_workflow_template
        )
        test_workflow_template_transition = WorkflowTransition.objects.create(
            origin_state=test_workflow_state_0,
            destination_state=test_workflow_state_1,
            workflow=test_workflow_template
        )

        WorkflowTransitionTriggerEvent.objects.create(
            event_type=test_stored_event_type,
            transition_id=test_workflow_template_transition.pk
        )
        WorkflowTransitionTriggerEvent.objects.create(
            event_type=test_stored_event_type,
            transition_id=test_workflow_template_transition.pk
        )
        self.assertTrue(WorkflowTransitionTriggerEvent.objects.count(), 2)

    def test_duplicated_workflow_template_transition_trigger_removal(self):
        WorkflowTransitionTriggerEvent = self.new_state.apps.get_model(
            app_label='document_states',
            model_name='WorkflowTransitionTriggerEvent'
        )

        self.assertTrue(WorkflowTransitionTriggerEvent.objects.count(), 1)
