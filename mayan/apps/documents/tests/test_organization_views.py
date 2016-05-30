from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import Document,DocumentType

from .literals import (
    TEST_DOCUMENT_TYPE, TEST_DOCUMENT_TYPE_2_LABEL,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_SMALL_DOCUMENT_CHECKSUM,
    TEST_SMALL_DOCUMENT_PATH
)


class DocumentOrganizationViewTestCase(OrganizationViewTestCase):
    def setUp(self):
        super(DocumentOrganizationViewTestCase, self).setUp()

        # Create a document for organization A
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.document_type = DocumentType.on_organization.create(
                label=TEST_DOCUMENT_TYPE
            )

            with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
                self.document = self.document_type.new_document(
                    file_object=file_object
                )

    def tearDown(self):
        super(DocumentOrganizationViewTestCase, self).tearDown()
        if self.document_type.pk:
            self.document_type.delete()

    def test_document_to_trash_view(self):
        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'documents:document_trash', args=(self.document.pk,)
            )
            self.assertEqual(response.status_code, 404)

    def test_document_view_view(self):
        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot find the document for
            # organization A
            response = self.get(
                'documents:document_properties', args=(self.document.pk,),
            )
            self.assertEqual(response.status_code, 404)

    def test_document_document_type_change_view(self):
        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            document_type = DocumentType.on_organization.create(
                label=TEST_DOCUMENT_TYPE_2_LABEL
            )

            response = self.post(
                'documents:document_document_type_edit',
                args=(self.document.pk,),
                data={'document_type': document_type.pk}
            )

            self.assertEqual(response.status_code, 403)
