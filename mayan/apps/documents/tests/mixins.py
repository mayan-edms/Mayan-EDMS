from __future__ import unicode_literals

import os

from django.conf import settings

from ..models import DocumentType

from .literals import (
    TEST_DOCUMENT_TYPE_DELETE_PERIOD, TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT,
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_PATH,
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


class DocumentTypeViewTestMixin(object):
    def _request_test_document_type_create_view(self):
        return self.post(
            viewname='documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL,
                'delete_time_period': TEST_DOCUMENT_TYPE_DELETE_PERIOD,
                'delete_time_unit': TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT
            }
        )

    def _request_test_document_type_delete_view(self):
        return self.post(
            viewname='documents:document_type_delete',
            kwargs={'pk': self.test_document_type.pk}
        )

    def _request_test_document_type_edit_view(self):
        return self.post(
            viewname='documents:document_type_edit',
            kwargs={'pk': self.test_document_type.pk},
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL_EDITED,
            }
        )

    def _request_test_document_type_list_view(self):
        return self.get(viewname='documents:document_type_list')


class DocumentTypeQuickLabelViewTestMixin(object):
    def _request_quick_label_create(self):
        return self.post(
            viewname='documents:document_type_filename_create',
            kwargs={'pk': self.test_document_type.pk},
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL,
            }
        )

    def _request_quick_label_delete(self):
        return self.post(
            viewname='documents:document_type_filename_delete',
            kwargs={'pk': self.test_document_type_filename.pk}
        )

    def _request_quick_label_edit(self):
        return self.post(
            viewname='documents:document_type_filename_edit',
            kwargs={'pk': self.test_document_type_filename.pk},
            data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
            }
        )

    def _request_quick_label_list_view(self):
        return self.get(
            viewname='documents:document_type_filename_list',
            kwargs={'pk': self.test_document_type.pk}
        )


class DocumentTypeQuickLabelTestMixin(object):
    def _create_test_quick_label(self):
        self.test_document_type_filename = self.test_document_type.filenames.create(
            filename=TEST_DOCUMENT_TYPE_QUICK_LABEL
        )


class DocumentVersionTestMixin(object):
    def _upload_new_version(self):
        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.test_document.new_version(
                comment=TEST_VERSION_COMMENT, file_object=file_object
            )
