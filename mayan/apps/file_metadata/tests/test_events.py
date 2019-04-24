from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.documents.tests.test_models import GenericDocumentTestCase

from ..events import (
    event_file_metadata_document_version_finish,
    event_file_metadata_document_version_submit
)


class FileMetadataEventsTestCase(GenericDocumentTestCase):
    def test_document_version_finish_event(self):
        Action.objects.all().delete()
        self.document.latest_version.submit_for_file_metadata_processing()

        # Get the most recent action
        action = Action.objects.order_by('-timestamp').first()

        self.assertEqual(
            action.target, self.document.latest_version
        )
        self.assertEqual(
            action.verb, event_file_metadata_document_version_finish.id
        )

    def test_document_version_submit_event(self):
        Action.objects.all().delete()
        self.document.latest_version.submit_for_file_metadata_processing()

        # Get the oldest action
        action = Action.objects.order_by('-timestamp').last()

        self.assertEqual(
            action.target, self.document.latest_version
        )
        self.assertEqual(
            action.verb, event_file_metadata_document_version_submit.id
        )
