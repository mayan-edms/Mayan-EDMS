from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_state_mixins import WorkflowTemplateStateActionTestMixin


class WorkflowTemplateCopyTestCase(
    DocumentTestMixin, ObjectCopyTestMixin,
    WorkflowTemplateStateActionTestMixin, WorkflowTemplateTestMixin,
    BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_state_action()
        self.test_object = self._test_workflow_template
