from actstream.models import Action

from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..events import (
    event_file_metadata_document_file_finish,
    event_file_metadata_document_file_submit
)


class FileMetadataEventsTestCase(GenericDocumentTestCase):
    def test_document_file_finish_event(self):
        Action.objects.all().delete()
        self.test_document.file_latest.submit_for_file_metadata_processing()

        # Get the most recent action
        action = Action.objects.order_by('-timestamp').first()

        self.assertEqual(
            action.target, self.test_document.file_latest
        )
        self.assertEqual(
            action.verb, event_file_metadata_document_file_finish.id
        )

    def test_document_file_submit_event(self):
        Action.objects.all().delete()
        self.test_document.file_latest.submit_for_file_metadata_processing()

        # Get the oldest action
        action = Action.objects.order_by('-timestamp').last()

        self.assertEqual(
            action.target, self.test_document.file_latest
        )
        self.assertEqual(
            action.verb, event_file_metadata_document_file_submit.id
        )
