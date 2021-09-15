from mayan.apps.testing.tests.base import BaseTestCase

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class WorkflowModelTestCase(WorkflowTemplateTestMixin, BaseTestCase):
    def test_workflow_template_preview(self):
        self._create_test_workflow_template()
        self.assertTrue(self.test_workflow_template.get_api_image_url())
