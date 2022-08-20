from mayan.apps.documents.events import (
    event_document_create, event_document_version_new
)
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.sources.models import WebFormSource
from mayan.apps.sources.tests.literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N
)
from mayan.apps.sources.wizards import WizardStep

from ..events import event_cabinet_add_document
from ..wizard_steps import WizardStepCabinets

from .mixins import CabinetDocumentUploadTestMixin, CabinetTestMixin


class CabinetDocumentUploadTestCase(
    CabinetTestMixin, CabinetDocumentUploadTestMixin,
    EventTestCaseMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super(CabinetDocumentUploadTestCase, self).setUp()
        self.test_source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )

    def tearDown(self):
        super(CabinetDocumentUploadTestCase, self).tearDown()
        WizardStep.reregister_all()

    def test_upload_interactive_view_with_access(self):
        self._create_test_cabinet()
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_create
        )

        self._clear_events()

        response = self._request_upload_interactive_document_create_view()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.test_cabinets[0] in Document.objects.first().cabinets.all()
        )
        self.assertTrue(
            self.test_cabinets[1] in Document.objects.first().cabinets.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        test_document = Document.objects.first()
        test_document_version = test_document.latest_version

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_create.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_version)
        self.assertEqual(events[1].verb, event_document_version_new.id)

        self.assertEqual(events[2].action_object, self.test_cabinets[0])
        self.assertEqual(events[2].actor, test_document)
        self.assertEqual(events[2].target, test_document)
        self.assertEqual(events[2].verb, event_cabinet_add_document.id)

        self.assertEqual(events[3].action_object, self.test_cabinets[1])
        self.assertEqual(events[3].actor, test_document)
        self.assertEqual(events[3].target, test_document)
        self.assertEqual(events[3].verb, event_cabinet_add_document.id)

    def test_upload_interactive_cabinet_selection_view_with_access(self):
        WizardStep.deregister_all()
        WizardStep.reregister(name=WizardStepCabinets.name)

        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_create
        )

        self._clear_events()

        response = self._request_wizard_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
