import os
import time

from django.conf import settings
from django.utils.module_loading import import_string

from mayan.apps.converter.classes import Layer
from mayan.apps.converter.layers import layer_saved_transformations

from ...models import Document, DocumentType, FavoriteDocument
from ...search import document_file_page_search, document_search

from ..literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_DOCUMENT_PATH,
    TEST_DOCUMENT_TYPE_DELETE_PERIOD, TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT,
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED,
    TEST_DOCUMENT_VERSION_COMMENT_EDITED, TEST_SMALL_DOCUMENT_FILENAME,
    TEST_SMALL_DOCUMENT_PATH, TEST_TRANSFORMATION_ARGUMENT,
    TEST_TRANSFORMATION_CLASS, TEST_VERSION_COMMENT
)


class DocumentVersionTestMixin:
    def _create_document_transformation(self):
        layer_saved_transformations.add_transformation_to(
            obj=self.test_document_version.pages.first(),
            transformation_class=TEST_TRANSFORMATION_CLASS,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )


class DocumentVersionTransformationViewTestMixin:
    def _request_test_document_clear_transformations_view(self):
        return self.post(
            viewname='documents:document_version_clear_transformations',
            kwargs={'document_id': self.test_document_version.pk}
        )

    def _request_test_document_multiple_clear_transformations(self):
        return self.post(
            viewname='documents:document_version_multiple_clear_transformations',
            data={'id_list': self.test_document_version.pk}
        )


class DocumentVersionViewTestMixin:
    def _request_test_document_version_edit_view(self):
        return self.post(
            viewname='documents:document_version_edit', kwargs={
                'document_version_id': self.test_document_version.pk
            }, data={
                'comment': TEST_DOCUMENT_VERSION_COMMENT_EDITED
            }
        )

    def _request_test_document_version_list_view(self):
        return self.get(
            viewname='documents:document_version_list', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_version_preview_view(self):
        return self.get(
            viewname='documents:document_version_preview', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )


class DocumentVersionPageRemapViewTestMixin:
    def _request_test_document_version_page_list_remap_view(self, data):
        return self.post(
            viewname='documents:document_version_page_list_remap', kwargs={
                'document_version_id': self.test_document_version.pk
            }, data=data
        )


class DocumentVersionPageResetViewTestMixin:
    def _request_test_document_version_page_list_reset_view(self):
        return self.post(
            viewname='documents:document_version_page_list_reset', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )
