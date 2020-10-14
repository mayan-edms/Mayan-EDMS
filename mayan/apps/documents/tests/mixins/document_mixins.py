import os

from django.conf import settings
from django.utils.module_loading import import_string

from mayan.apps.converter.classes import Layer

from ...literals import DOCUMENT_FILE_ACTION_PAGES_NEW
from ...models import Document, DocumentType
from ...search import document_file_page_search, document_search

from ..literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_DOCUMENT_PATH,
    TEST_DOCUMENT_TYPE_LABEL, TEST_SMALL_DOCUMENT_FILENAME,
)


class DocumentAPIViewTestMixin:
    def _request_test_document_api_download_view(self):
        return self.get(
            viewname='rest_api:document-download', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_api_upload_view(self):
        with open(file=TEST_DOCUMENT_PATH, mode='rb') as file_object:
            return self.post(
                viewname='rest_api:document-list', data={
                    'document_type': self.test_document_type.pk,
                    'file': file_object
                }
            )

    def _request_test_document_description_api_edit_via_patch_view(self):
        return self.patch(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_description_api_edit_via_put_view(self):
        return self.put(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_document_type_change_api_view(self):
        return self.post(
            viewname='rest_api:document-type-change', kwargs={
                'pk': self.test_document.pk
            }, data={'new_document_type': self.test_document_type_2.pk}
        )


class DocumentSearchTestMixin:
    search_backend = import_string(
        dotted_path='mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'
    )()

    def _perform_document_file_page_search(self):
        return self.search_backend.search(
            search_model=document_file_page_search, query_string={'q': self.test_document.label},
            user=self._test_case_user
        )

    def _perform_document_search(self):
        return self.search_backend.search(
            search_model=document_search, query_string={'q': self.test_document.label},
            user=self._test_case_user
        )


class DocumentTestMixin:
    auto_create_test_document_type = True
    auto_upload_test_document = True
    test_document_file_filename = TEST_SMALL_DOCUMENT_FILENAME
    test_document_file_path = None
    test_document_filename = TEST_SMALL_DOCUMENT_FILENAME
    test_document_language = None
    test_document_path = None

    def setUp(self):
        super().setUp()
        Layer.invalidate_cache()

        self.test_documents = []

        if self.auto_create_test_document_type:
            self._create_test_document_type()

            if self.auto_upload_test_document:
                self._upload_test_document()

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super(DocumentTestMixin, self).tearDown()

    def _create_test_document_stub(self):
        self.test_document_stub = Document.objects.create(
            document_type=self.test_document_type, label='document_stub'
        )

    def _create_test_document_type(self):
        self.test_document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

    def _calculate_test_document_path(self):
        if not self.test_document_path:
            self.test_document_path = os.path.join(
                settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
                'sample_documents', self.test_document_filename
            )

    def _calculate_test_document_file_path(self):
        if not self.test_document_file_path:
            self.test_document_file_path = os.path.join(
                settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
                'sample_documents', self.test_document_file_filename
            )

    def _upload_test_document(self, label=None, _user=None):
        self._calculate_test_document_path()

        if not label:
            label = self.test_document_filename

        with open(file=self.test_document_path, mode='rb') as file_object:
            document, document_file = self.test_document_type.new_document(
                file_object=file_object, label=label,
                language=self.test_document_language, _user=_user
            )

        self.test_document = document
        self.test_documents.append(document)

        self.test_document_file_page = document_file.pages.first()
        self.test_document_file = document_file
        self.test_document_version = self.test_document.latest_version

    def _upload_test_document_file(self, action=None, _user=None):
        self._calculate_test_document_file_path()

        if not action:
            action = DOCUMENT_FILE_ACTION_PAGES_NEW

        with open(file=self.test_document_path, mode='rb') as file_object:
            self.test_document_file = self.test_document.new_file(
                action=action, file_object=file_object, _user=_user
            )

        self.test_document_file_page = self.test_document_file.pages.first()
        self.test_document_version = self.test_document.latest_version


class DocumentViewTestMixin:
    def _request_test_document_list_view(self):
        return self.get(viewname='documents:document_list')

    def _request_test_document_preview_view(self):
        return self.get(
            viewname='documents:document_preview', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_print_view(self):
        return self.get(
            viewname='documents:document_print', kwargs={
                'document_id': self.test_document.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_type_change_get_view(self):
        return self.get(
            viewname='documents:document_type_change', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_type_change_post_view(self, document_type):
        return self.post(
            viewname='documents:document_type_change', kwargs={
                'document_id': self.test_document.pk
            }, data={'document_type': document_type.pk}
        )

    def _request_test_document_multiple_type_change(self, document_type):
        return self.post(
            viewname='documents:document_multiple_type_change',
            data={
                'id_list': self.test_document.pk,
                'document_type': document_type.pk
            }
        )
