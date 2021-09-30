from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.sources.tests.mixins.web_form_source_mixins import WebFormSourceTestMixin

from .mixins import TagTestMixin, TaggedDocumentUploadWizardStepViewTestMixin


class TaggedDocumentUploadViewTestCase(
    TaggedDocumentUploadWizardStepViewTestMixin, TagTestMixin,
    WebFormSourceTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_upload_interactive_view_with_full_access(self):
        self._create_test_tag()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        response = self._request_upload_interactive_document_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.test_tag in Document.objects.first().tags.all())

    def test_upload_interactive_multiple_tags_view_full_access(self):
        self._create_test_tag()
        self._create_test_tag()

        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self.test_source, permission=permission_document_create
        )

        response = self._request_upload_interactive_document_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_tags[0] in Document.objects.first().tags.all()
        )
        self.assertTrue(
            self.test_tags[1] in Document.objects.first().tags.all()
        )
