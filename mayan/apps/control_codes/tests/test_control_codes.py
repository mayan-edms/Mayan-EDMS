from __future__ import unicode_literals

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.storage.utils import fs_cleanup, mkstemp

from ..control_codes import ControlCodeAttributeEdit

TEST_ATTRIBUTE_VALUE = 'test value'


class ControlCodeAttributeEditTestCase(GenericDocumentTestCase):
    auto_upload_document = False

    def setUp(self):
        super(ControlCodeAttributeEditTestCase, self).setUp()
        self.test_document_path = mkstemp()[1]

    def tearDown(self):
        fs_cleanup(filename=self.test_document_path)
        super(ControlCodeAttributeEditTestCase, self).tearDown()

    def test_control_code(self):
        with open(self.test_document_path, mode='wb') as file_object:
            control_code = ControlCodeAttributeEdit(
                name='label', value=TEST_ATTRIBUTE_VALUE
            )
            control_code.get_image().save(file_object)

        self.upload_document()
        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.label, TEST_ATTRIBUTE_VALUE)
