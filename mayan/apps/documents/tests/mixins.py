from __future__ import unicode_literals

import os

from django.conf import settings

from ..models import DocumentType

from .literals import TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_FILENAME


class DocumentTestMixin(object):
    auto_create_document_type = True
    auto_upload_document = True
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME

    def create_document_type(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def upload_document(self):
        with open(self.test_document_path) as file_object:
            document = self.document_type.new_document(
                file_object=file_object, label=self.test_document_filename
            )
        return document

    def setUp(self):
        super(DocumentTestMixin, self).setUp()
        self.test_document_path = os.path.join(
            settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
            'sample_documents', self.test_document_filename
        )

        if self.auto_create_document_type:
            self.create_document_type()

            if self.auto_upload_document:
                self.document = self.upload_document()

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super(DocumentTestMixin, self).tearDown()
