from actstream.models import Action

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..events import (
    event_ocr_document_version_content_deleted,
    event_ocr_document_version_submit, event_ocr_document_version_finish
)
from ..models import DocumentVersionPageOCRContent


class DocumentVersionOCREventsTestCase(GenericDocumentTestCase):
    def test_document_content_deleted_event(self):
        Action.objects.all().delete()
        DocumentVersionPageOCRContent.objects.delete_content_for(
            document_version=self.test_document_version
        )

        # Get the oldest action
        action = Action.objects.order_by('-timestamp').last()

        self.assertEqual(
            action.target, self.test_document_version
        )
        self.assertEqual(
            action.action_object, self.test_document
        )
        self.assertEqual(
            action.verb, event_ocr_document_version_content_deleted.id
        )

    def test_document_version_submit_event(self):
        Action.objects.all().delete()
        self.test_document.submit_for_ocr()

        # Get the oldest action
        action = Action.objects.order_by('-timestamp').last()

        self.assertEqual(
            action.target, self.test_document.version_active
        )
        self.assertEqual(
            action.action_object, self.test_document
        )
        self.assertEqual(
            action.verb, event_ocr_document_version_submit.id
        )

    def test_document_version_finish_event(self):
        Action.objects.all().delete()
        self.test_document.submit_for_ocr()

        # Get the most recent action
        action = Action.objects.order_by('-timestamp').first()

        self.assertEqual(
            action.target, self.test_document.version_active
        )
        self.assertEqual(
            action.action_object, self.test_document
        )
        self.assertEqual(
            action.verb, event_ocr_document_version_finish.id
        )
