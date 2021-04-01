import os

from django.conf import settings
from django.db.models import Q
from django.utils.module_loading import import_string

from mayan.apps.converter.classes import Layer

from ...literals import DOCUMENT_FILE_ACTION_PAGES_NEW, PAGE_RANGE_ALL
from ...models import Document, DocumentType
from ...search import document_file_page_search, document_search

from ..literals import (
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_DOCUMENT_TYPE_LABEL,
    TEST_SMALL_DOCUMENT_FILENAME, TEST_SMALL_DOCUMENT_PATH
)


class DocumentAPIViewTestMixin:
    def _request_test_document_change_type_api_view(self):
        return self.post(
            viewname='rest_api:document-change-type', kwargs={
                'document_id': self.test_document.pk
            }, data={'document_type_id': self.test_document_type_2.pk}
        )

    def _request_test_document_create_api_view(self):
        pk_list = list(Document.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:document-list', data={
                'document_type_id': self.test_document_type.pk
            }
        )

        try:
            self.test_document = Document.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Document.DoesNotExist:
            self.test_document = None

        return response

    def _request_test_document_detail_api_view(self):
        return self.get(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self.test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_list_api_view(self):
        return self.get(viewname='rest_api:document-list')

    def _request_test_document_upload_api_view(self):
        pk_list = list(Document.objects.values_list('pk', flat=True))

        with open(file=TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            response = self.post(
                viewname='rest_api:document-upload', data={
                    'document_type_id': self.test_document_type.pk,
                    'file': file_object
                }
            )

        try:
            self.test_document = Document.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Document.DoesNotExist:
            self.test_document = None

        return response


class DocumentSearchTestMixin:
    search_backend = import_string(
        dotted_path='mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'
    )()

    def _perform_document_file_page_search(self):
        return self.search_backend.search(
            search_model=document_file_page_search,
            query_string={'q': self.test_document.label},
            user=self._test_case_user
        )

    def _perform_document_search(self):
        return self.search_backend.search(
            search_model=document_search,
            query_string={'q': self.test_document.label},
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
        self.test_document_types = []

        if self.auto_create_test_document_type:
            self._create_test_document_type()

            if self.auto_upload_test_document:
                self._upload_test_document()

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super().tearDown()

    def _create_test_document_stub(self, document_type=None, label=None):
        self.test_document_stub = Document.objects.create(
            document_type=document_type or self.test_document_type,
            label=label or 'document_stub'
        )
        self.test_document = self.test_document_stub
        self.test_documents.append(self.test_document)

    def _create_test_document_type(self, label=None):
        total_document_types = len(self.test_document_types)
        label = label or '{}_{}'.format(
            TEST_DOCUMENT_TYPE_LABEL, total_document_types
        )

        self.test_document_type = DocumentType.objects.create(label=label)
        self.test_document_types.append(self.test_document_type)

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

    def _upload_test_document(self, document_type=None, label=None, _user=None):
        self._calculate_test_document_path()

        if not label:
            label = self.test_document_filename

        document_type = document_type or self.test_document_type

        with open(file=self.test_document_path, mode='rb') as file_object:
            document, document_file = document_type.new_document(
                file_object=file_object, label=label,
                language=self.test_document_language, _user=_user
            )

        self.test_document = document
        self.test_documents.append(document)

        self.test_document_file = document_file
        self.test_document_file_page = document_file.file_pages.first()
        self.test_document_version = self.test_document.version_active
        self.test_document_version_page = self.test_document_version.version_pages.first()

    def _upload_test_document_file(self, action=None, _user=None):
        self._calculate_test_document_file_path()

        if not action:
            action = DOCUMENT_FILE_ACTION_PAGES_NEW

        with open(file=self.test_document_path, mode='rb') as file_object:
            self.test_document_file = self.test_document.file_new(
                action=action, file_object=file_object, _user=_user
            )

        self.test_document_file_page = self.test_document_file.pages.first()
        self.test_document_version = self.test_document.version_active


class DocumentViewTestMixin:
    def _request_test_document_list_view(self):
        return self.get(viewname='documents:document_list')

    def _request_test_document_preview_view(self):
        return self.get(
            viewname='documents:document_preview', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_print_form_view(self):
        return self.get(
            viewname='documents:document_print_form', kwargs={
                'document_id': self.test_document.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_print_view(self):
        return self.get(
            viewname='documents:document_print_view', kwargs={
                'document_id': self.test_document.pk,
            }, query={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_properties_edit_get_view(self):
        return self.get(
            viewname='documents:document_properties_edit', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_properties_view(self):
        return self.get(
            viewname='documents:document_properties', kwargs={
                'document_id': self.test_document.pk
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
