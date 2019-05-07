from __future__ import unicode_literals

import os

from django.conf import settings

from ..models import DocumentType

from .literals import (
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_SMALL_DOCUMENT_PATH,
    TEST_VERSION_COMMENT
)

__all__ = ('DocumentTestMixin',)


class DocumentTestMixin(object):
    auto_create_document_type = True
    auto_upload_document = True
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
    test_document_path = None

    def _create_document_type(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )
        self.test_document_type = self.test_document_type

    def upload_document(self, label=None):
        self._calculate_test_document_path()

        if not label:
            label = self.test_document_filename

        with open(self.test_document_path, mode='rb') as file_object:
            document = self.test_document_type.new_document(
                file_object=file_object, label=label
            )

        self.test_document = document
        self.test_documents.append(document)

    def _calculate_test_document_path(self):
        if not self.test_document_path:
            self.test_document_path = os.path.join(
                settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
                'sample_documents', self.test_document_filename
            )

    def setUp(self):
        super(DocumentTestMixin, self).setUp()
        self.test_documents = []

        if self.auto_create_document_type:
            self._create_document_type()

            if self.auto_upload_document:
                self.upload_document()

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super(DocumentTestMixin, self).tearDown()


class DocumentVersionTestMixin(object):
    def _upload_new_version(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(
                comment=TEST_VERSION_COMMENT, file_object=file_object
            )


class DocumentTypeQuickLabelTestMixin(object):
    def _create_test_quick_label(self):
        self.test_document_type_filename = self.test_document_type.filenames.create(
            filename=TEST_DOCUMENT_TYPE_QUICK_LABEL
        )
