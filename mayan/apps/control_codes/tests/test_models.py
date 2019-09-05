from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins import ControlSheetCodeTestMixin

TEST_CONTROL_CODE_DOCUMENT_PATH = '/tmp/test_control_code.png'


class ControlCodeTestCase(ControlSheetCodeTestMixin, GenericDocumentTestCase):
    auto_upload_document = False
    test_document_path = TEST_CONTROL_CODE_DOCUMENT_PATH

    def test_control_code_detection(self):
        with open(TEST_CONTROL_CODE_DOCUMENT_PATH, mode='wb') as file_object:
            control_code = self._test_control_code_class(
                argument_1='test argument value'
            )
            control_code.image.save(file_object)

        self.upload_document()

        print self.test_document.pages.count()
