from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.documents.tests.test_models import GenericDocumentTestCase

from ..events import (
    event_cabinets_add_document, event_cabinets_remove_document
)

from .mixins import CabinetTestMixin


class CabinetsEventsTestCase(CabinetTestMixin, GenericDocumentTestCase):
    def setUp(self):
        super(CabinetsEventsTestCase, self).setUp()
        self._create_test_cabinet()

    def test_document_cabinet_add_event(self):
        Action.objects.all().delete()
        self.test_cabinet.add_document(document=self.test_document)

        self.assertEqual(Action.objects.last().target, self.test_document)
        self.assertEqual(
            Action.objects.last().verb,
            event_cabinets_add_document.id
        )

    def test_document_cabinet_remove_event(self):
        self.test_cabinet.add_document(document=self.test_document)
        Action.objects.all().delete()
        self.test_cabinet.remove_document(document=self.test_document)

        self.assertEqual(Action.objects.first().target, self.test_document)
        self.assertEqual(
            Action.objects.first().verb,
            event_cabinets_remove_document.id
        )
