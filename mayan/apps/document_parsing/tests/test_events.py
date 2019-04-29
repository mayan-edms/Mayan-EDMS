from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.documents.tests.literals import TEST_PDF_DOCUMENT_FILENAME
from mayan.apps.documents.tests.test_models import GenericDocumentTestCase

from ..events import (
    event_parsing_document_version_submit,
    event_parsing_document_version_finish
)


class DocumentParsingEventsTestCase(GenericDocumentTestCase):
    # Ensure we use a PDF file
    test_document_filename = TEST_PDF_DOCUMENT_FILENAME

    def test_document_version_submit_event(self):
        Action.objects.all().delete()
        self.test_document.submit_for_parsing()

        self.assertEqual(
            Action.objects.last().target, self.test_document.latest_version
        )
        self.assertEqual(
            Action.objects.last().verb,
            event_parsing_document_version_submit.id
        )

    def test_document_version_finish_event(self):
        Action.objects.all().delete()
        self.test_document.submit_for_parsing()
        self.assertEqual(
            Action.objects.first().target, self.test_document.latest_version
        )
        self.assertEqual(
            Action.objects.first().verb,
            event_parsing_document_version_finish.id
        )
