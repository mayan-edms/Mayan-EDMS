from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..forms import DocumentMetadataForm

from .mixins import MetadataTypeTestMixin


class DocumentMetadataFormTestCase(
    DocumentTestMixin, MetadataTypeTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()

        self._create_test_document_stub()
        self._create_test_metadata_type(
            add_test_document_type=True, required=True
        )

    def test_document_metadata_form_empty_required(self):
        form = DocumentMetadataForm(
            data={'update': True},
            initial={
                'document_type': self.test_document_type,
                'metadata_type': self.test_metadata_type
            }
        )

        # Trigger clean method.
        errors = form.errors

        self.assertEqual(
            errors['__all__'],
            ['"test metadata type label_0" is required for this document type.']
        )
        self.assertEqual(
            errors['metadata_type_id'], ['This field is required.']
        )
        self.assertEqual(
            errors['value'], ['This field is required.']
        )
