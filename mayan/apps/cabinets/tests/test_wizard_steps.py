from __future__ import unicode_literals

from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests import (
    GenericDocumentViewTestCase, TEST_SMALL_DOCUMENT_PATH,
)
from mayan.apps.sources.models import WebFormSource
from mayan.apps.sources.tests.literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N
)
from mayan.apps.sources.wizards import WizardStep

from ..models import Cabinet
from ..wizard_steps import WizardStepCabinets

from .mixins import CabinetTestMixin


class CabinetDocumentUploadTestCase(CabinetTestMixin, GenericDocumentViewTestCase):
    auto_upload_document = False

    def setUp(self):
        super(CabinetDocumentUploadTestCase, self).setUp()
        self.test_source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )

    def tearDown(self):
        super(CabinetDocumentUploadTestCase, self).tearDown()
        WizardStep.reregister_all()

    def _request_upload_interactive_document_create_view(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:upload_interactive', kwargs={
                    'source_id': self.test_source.pk
                }, data={
                    'document_type_id': self.test_document_type.pk,
                    'source-file': file_object,
                    'cabinets': Cabinet.objects.values_list('pk', flat=True)
                }
            )

    def test_upload_interactive_view_with_access(self):
        self._create_test_cabinet()
        self._create_test_cabinet()
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        response = self._request_upload_interactive_document_create_view()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.test_cabinets[0] in Document.objects.first().cabinets.all()
        )
        self.assertTrue(
            self.test_cabinets[1] in Document.objects.first().cabinets.all()
        )

    def _request_wizard_view(self):
        return self.get(viewname='sources:document_create_multiple')

    def test_upload_interactive_cabinet_selection_view_with_access(self):
        WizardStep.deregister_all()
        WizardStep.reregister(name=WizardStepCabinets.name)

        self._create_test_cabinet()
        self.grant_access(
            permission=permission_document_create, obj=self.test_document_type

        )

        response = self._request_wizard_view()
        self.assertEqual(response.status_code, 200)
