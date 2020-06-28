from mayan.apps.common.tests.mixins import ObjectCopyTestMixin
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import WorkflowStateActionTestMixin, WorkflowTestMixin


class WorkflowTemplateCopyTestCase(
    DocumentTestMixin, ObjectCopyTestMixin, WorkflowStateActionTestMixin,
    WorkflowTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._create_test_workflow_state_action()
        self.test_workflow.document_types.add(self.test_document_type)
        self.test_object = self.test_workflow
