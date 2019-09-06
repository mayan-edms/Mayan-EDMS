from __future__ import unicode_literals

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.storage.utils import fs_cleanup, mkstemp

from ..control_codes import ControlCodeDocumentMetadataAdd

from .literals import TEST_DOCUMENT_METADATA_VALUE_2
from .mixins import DocumentMetadataViewTestMixin, MetadataTypeTestMixin


class ControlCodeDocumentMetadataAddTestCase(
    DocumentMetadataViewTestMixin, MetadataTypeTestMixin,
    GenericDocumentTestCase
):
    auto_upload_document = False

    def setUp(self):
        super(ControlCodeDocumentMetadataAddTestCase, self).setUp()
        self.test_document_path = mkstemp()[1]

        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )

    def tearDown(self):
        fs_cleanup(filename=self.test_document_path)
        super(ControlCodeDocumentMetadataAddTestCase, self).tearDown()

    def test_control_code(self):
        with open(self.test_document_path, mode='wb') as file_object:
            control_code = ControlCodeDocumentMetadataAdd(
                name=self.test_metadata_type.name,
                value=TEST_DOCUMENT_METADATA_VALUE_2
            )
            control_code.get_image().save(file_object)

        self.upload_document()
        self.assertEqual(
            self.test_document.metadata.first().value, TEST_DOCUMENT_METADATA_VALUE_2
        )
