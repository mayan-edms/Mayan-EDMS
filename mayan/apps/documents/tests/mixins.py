from __future__ import unicode_literals

import os

from django.conf import settings

from ..models import DocumentType

from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_DOCUMENT_TYPE_QUICK_LABEL
)

__all__ = ('DocumentTestMixin',)


class DocumentTestMixin(object):
    auto_create_document_type = True
    auto_upload_document = True
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME

    def _create_document_type(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def upload_document(self):
        self._calculate_test_document_path()

        with open(self.test_document_path, mode='rb') as file_object:
            document = self.document_type.new_document(
                file_object=file_object, label=self.test_document_filename
            )
        return document

    def _calculate_test_document_path(self):
        self.test_document_path = os.path.join(
            settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
            'sample_documents', self.test_document_filename
        )

    def setUp(self):
        super(DocumentTestMixin, self).setUp()

        if self.auto_create_document_type:
            self._create_document_type()

            if self.auto_upload_document:
                self.document = self.upload_document()

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super(DocumentTestMixin, self).tearDown()


class DocumentTypeQuickLabelTestMixin(object):
    def _create_quick_label(self):
        self.document_type_filename = self.document_type.filenames.create(
            filename=TEST_DOCUMENT_TYPE_QUICK_LABEL
        )
