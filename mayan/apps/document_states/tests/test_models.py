from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins import WorkflowTestMixin


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


class WorkflowModelTestCase(WorkflowTestMixin, BaseTestCase):
    def test_workflow_template_preview(self):
        self._create_test_workflow()
        self.assertTrue(self.test_workflow.get_api_image_url())
