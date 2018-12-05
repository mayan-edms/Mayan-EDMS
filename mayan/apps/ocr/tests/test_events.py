from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.documents.tests.test_models import GenericDocumentTestCase

from ..events import (
    event_ocr_document_version_submit, event_ocr_document_version_finish
)


class OCREventsTestCase(GenericDocumentTestCase):
    def test_document_version_submit_event(self):
        Action.objects.all().delete()
        self.document.submit_for_ocr()

        # Get the oldest action
        action = Action.objects.order_by('-timestamp').last()

        self.assertEqual(
            action.target, self.document.latest_version
        )
        self.assertEqual(
            action.verb, event_ocr_document_version_submit.id
        )

    def test_document_version_finish_event(self):
        Action.objects.all().delete()
        self.document.submit_for_ocr()

        # Get the most recent action
        action = Action.objects.order_by('-timestamp').first()

        self.assertEqual(
            action.target, self.document.latest_version
        )
        self.assertEqual(
            action.verb, event_ocr_document_version_finish.id
        )
