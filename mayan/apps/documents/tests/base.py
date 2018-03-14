# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import override_settings

from common.tests import GenericViewTestCase

from ..models import DocumentType

from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_SMALL_DOCUMENT_PATH,
)


@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentViewTestCase(GenericViewTestCase):
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
    test_document_path = TEST_SMALL_DOCUMENT_PATH

    def setUp(self):
        super(GenericDocumentViewTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        with open(self.test_document_path) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object, label=self.test_document_filename
            )

    def tearDown(self):
        if self.document_type.pk:
            self.document_type.delete()
        super(GenericDocumentViewTestCase, self).tearDown()
