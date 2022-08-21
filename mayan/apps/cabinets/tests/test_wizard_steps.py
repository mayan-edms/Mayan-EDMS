from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.sources.tests.mixins.web_form_source_mixins import WebFormSourceBackendTestMixin
from mayan.apps.sources.wizards import DocumentCreateWizardStep

from ..events import event_cabinet_document_added
from ..wizard_steps import DocumentCreateWizardStepCabinets

from .mixins import (
    CabinetDocumentUploadWizardStepTestMixin, CabinetTestMixin
)


class CabinetDocumentUploadTestCase(
    CabinetTestMixin, CabinetDocumentUploadWizardStepTestMixin,
    WebFormSourceBackendTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def tearDown(self):
        super().tearDown()
        DocumentCreateWizardStep.reregister_all()

    def test_upload_interactive_view_with_access(self):
        self._create_test_cabinet()
        self._create_test_cabinet()

        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        self._clear_events()

        response = self._request_upload_interactive_document_create_view()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self._test_cabinets[0] in Document.objects.first().cabinets.all()
        )
        self.assertTrue(
            self._test_cabinets[1] in Document.objects.first().cabinets.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 7)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_version)
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_page)
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[5].action_object, self._test_cabinets[0])
        self.assertEqual(events[5].actor, test_document)
        self.assertEqual(events[5].target, test_document)
        self.assertEqual(events[5].verb, event_cabinet_document_added.id)

        self.assertEqual(events[6].action_object, self._test_cabinets[1])
        self.assertEqual(events[6].actor, test_document)
        self.assertEqual(events[6].target, test_document)
        self.assertEqual(events[6].verb, event_cabinet_document_added.id)

    def test_upload_interactive_cabinet_selection_view_with_access(self):
        DocumentCreateWizardStep.deregister_all()
        DocumentCreateWizardStep.reregister(
            name=DocumentCreateWizardStepCabinets.name
        )

        self._create_test_cabinet()
        self.grant_access(
            obj=self._test_document_type,
            permission=permission_document_create
        )

        self._clear_events()

        response = self._request_wizard_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
