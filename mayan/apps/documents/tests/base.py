# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.conf import settings
from django.test import override_settings

from common.tests import BaseTestCase, GenericViewTestCase

from ..models import DocumentType

from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_SMALL_DOCUMENT_PATH,
)


@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentTestCase(BaseTestCase):
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME

    def upload_document(self):
        with open(self.test_document_path) as file_object:
            document = self.document_type.new_document(
                file_object=file_object, label=self.test_document_filename
            )
        return document

    def setUp(self):
        super(GenericDocumentTestCase, self).setUp()
        self.test_document_path = os.path.join(
            settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
            'sample_documents', self.test_document_filename
        )

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        self.document = self.upload_document()

    def tearDown(self):
        self.document_type.delete()
        super(GenericDocumentTestCase, self).tearDown()


@override_settings(OCR_AUTO_OCR=False)
class GenericDocumentViewTestCase(GenericViewTestCase):
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
    test_document_path = TEST_SMALL_DOCUMENT_PATH

    def upload_document(self):
        with open(self.test_document_path) as file_object:
            document = self.document_type.new_document(
                file_object=file_object, label=self.test_document_filename
            )
        return document

    def setUp(self):
        super(GenericDocumentViewTestCase, self).setUp()
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.document = self.upload_document()

    def tearDown(self):
        if self.document_type.pk:
            self.document_type.delete()
        super(GenericDocumentViewTestCase, self).tearDown()
