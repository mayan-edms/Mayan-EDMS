from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase

from .mixins import WorkflowTestMixin


class WorkflowModelTestCase(WorkflowTestMixin, BaseTestCase):
    def test_workflow_template_preview(self):
        self._create_test_workflow()
        self.assertTrue(self.test_workflow.get_api_image_url())
