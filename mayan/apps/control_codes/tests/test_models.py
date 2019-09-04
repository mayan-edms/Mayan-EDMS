from __future__ import unicode_literals

from django.test import override_settings

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from ..classes import ControlCode
from ..models import ControlSheet

TEST_CONTROL_CODE_DOCUMENT_PATH = '/tmp/test_control_code.png'


class ControlCodeTest(ControlCode):
    arguments = ('argument_1',)
    label = 'Test'
    name = 'test'

    def execute(self):
        pass


ControlCode.register(control_code=ControlCodeTest)


class ControlCodeTestCase(GenericDocumentTestCase):
    auto_upload_document = False
    test_document_path = TEST_CONTROL_CODE_DOCUMENT_PATH

    def test_control_code_detection(self):
        with open(TEST_CONTROL_CODE_DOCUMENT_PATH, mode='wb') as file_object:
            control_code = ControlCodeTest(argument_1='test argument value')
            control_code.image.save(file_object)

        self.upload_document()

        print self.test_document.pages.count()
