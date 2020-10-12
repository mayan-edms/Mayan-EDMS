from actstream.models import Action

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import TEST_PDF_DOCUMENT_FILENAME

from ..events import (
    event_parsing_document_file_content_deleted,
    event_parsing_document_file_finish, event_parsing_document_file_submit
)
from ..models import DocumentFilePageContent


class DocumentFileParsingEventsTestCase(GenericDocumentTestCase):
    # Ensure we use a PDF file
    test_document_file_filename = TEST_PDF_DOCUMENT_FILENAME

    def test_document_file_content_deleted_event(self):
        Action.objects.all().delete()
        DocumentFilePageContent.objects.delete_content_for(
            document_file=self.test_document_file
        )

        # Get the oldest action
        action = Action.objects.order_by('-timestamp').last()

        self.assertEqual(
            action.target, self.test_document_file
        )
        self.assertEqual(
            action.verb, event_parsing_document_file_content_deleted.id
        )

    def test_document_file_file_submit_event(self):
        Action.objects.all().delete()
        self.test_document_file.submit_for_parsing()

        self.assertEqual(
            Action.objects.last().target, self.test_document_file
        )
        self.assertEqual(
            Action.objects.last().verb,
            event_parsing_document_file_submit.id
        )

    def test_document_file_file_finish_event(self):
        Action.objects.all().delete()
        self.test_document_file.submit_for_parsing()
        self.assertEqual(
            Action.objects.first().target, self.test_document_file
        )
        self.assertEqual(
            Action.objects.first().verb,
            event_parsing_document_file_finish.id
        )
