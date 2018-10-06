from __future__ import unicode_literals

from documents.models import Document
from documents.permissions import permission_document_create
from documents.tests import (
    GenericDocumentViewTestCase, TEST_SMALL_DOCUMENT_PATH,
)
from sources.models import WebFormSource
from sources.tests.literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N
)
from sources.wizards import WizardStep

from ..models import Cabinet
from ..wizard_steps import WizardStepCabinets

from .literals import TEST_CABINET_LABEL


class CabinetDocumentUploadTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(CabinetDocumentUploadTestCase, self).setUp()
        self.login_user()
        self.source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )

        self.document.delete()

    def tearDown(self):
        super(CabinetDocumentUploadTestCase, self).tearDown()
        WizardStep.reregister_all()

    def _request_upload_interactive_document_create_view(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:upload_interactive', args=(self.source.pk,),
                data={
                    'document_type_id': self.document_type.pk,
                    'source-file': file_object,
                    'cabinets': self.cabinet.pk
                }
            )

    def _create_cabinet(self):
        self.cabinet = Cabinet.objects.create(label=TEST_CABINET_LABEL)

    def test_upload_interactive_view_with_access(self):
        self._create_cabinet()
        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        response = self._request_upload_interactive_document_create_view()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.cabinet in Document.objects.first().cabinets.all())

    def _request_wizard_view(self):
        return self.get(viewname='sources:document_create_multiple')

    def test_upload_interactive_cabinet_selection_view_with_access(self):
        WizardStep.deregister_all()
        WizardStep.reregister(name=WizardStepCabinets.name)

        self._create_cabinet()
        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        response = self._request_wizard_view()
        self.assertEqual(response.status_code, 200)
