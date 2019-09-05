from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..control_codes import ControlCodeAttributeEdit

from .mixins import ControlSheetCodeTestMixin

#TODO: use mktmp
TEST_CONTROL_CODE_DOCUMENT_PATH = '/tmp/test_control_code.png'

"""
class ControlCodeTestCase(ControlSheetCodeTestMixin, GenericDocumentTestCase):
    auto_upload_document = False
    test_document_path = TEST_CONTROL_CODE_DOCUMENT_PATH

    def test_control_code_detection(self):
        with open(TEST_CONTROL_CODE_DOCUMENT_PATH, mode='wb') as file_object:
            control_code = self._test_control_code_class(
                argument_1='test argument value'
            )
            control_code.get_image().save(file_object)

        self.upload_document()

        print self.test_document.pages.count()
"""

class ControlCodeAttributeEditTestCase(GenericDocumentTestCase):
    auto_upload_document = False
    test_document_path = TEST_CONTROL_CODE_DOCUMENT_PATH

    def test_control_code(self):
        TEST_ATTRIBUTE_VALUE = 'test value'

        with open(TEST_CONTROL_CODE_DOCUMENT_PATH, mode='wb') as file_object:
            control_code = ControlCodeAttributeEdit(
                attribute='label', value=TEST_ATTRIBUTE_VALUE
            )
            control_code.get_image().save(file_object)

        self.upload_document()
        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.label, TEST_ATTRIBUTE_VALUE)
