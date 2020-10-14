from mayan.apps.documents.tests.base import GenericDocumentTestCase


class ActionTestCase(GenericDocumentTestCase):
    def setUp(self):
        super(ActionTestCase, self).setUp()

        class MockWorkflowInstance:
            document = self.test_document

        class MockEntryLog:
            workflow_instance = MockWorkflowInstance()

        self.entry_log = MockEntryLog()
