import os

from django.conf import settings
from django.db.models import Q

from mayan.apps.converter.classes import Layer

from ...literals import PAGE_RANGE_ALL
from ...models import Document, DocumentType

from ..literals import (
    DEFAULT_DOCUMENT_STUB_LABEL, TEST_DOCUMENT_DESCRIPTION,
    TEST_DOCUMENT_DESCRIPTION_EDITED, TEST_DOCUMENT_TYPE_LABEL,
    TEST_FILE_SMALL_FILENAME, TEST_FILE_SMALL_PATH
)


class DocumentAPIViewTestMixin:
    def _request_test_document_change_type_api_view(self):
        return self.post(
            viewname='rest_api:document-change-type', kwargs={
                'document_id': self._test_document.pk
            }, data={'document_type_id': self._test_document_types[1].pk}
        )

    def _request_test_document_create_api_view(self):
        pk_list = list(Document.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='rest_api:document-list', data={
                'document_type_id': self._test_document_type.pk
            }
        )

        try:
            self._test_document = Document.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Document.DoesNotExist:
            self._test_document = None

        return response

    def _request_test_document_detail_api_view(self):
        return self.get(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self._test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self._test_document.pk
            }, data={'description': TEST_DOCUMENT_DESCRIPTION_EDITED}
        )

    def _request_test_document_list_api_view(self):
        return self.get(viewname='rest_api:document-list')

    def _request_test_document_upload_api_view(self):
        pk_list = list(Document.objects.values_list('pk', flat=True))

        with open(file=TEST_FILE_SMALL_PATH, mode='rb') as file_object:
            response = self.post(
                viewname='rest_api:document-upload', data={
                    'document_type_id': self._test_document_type.pk,
                    'file': file_object
                }
            )

        try:
            self._test_document = Document.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Document.DoesNotExist:
            self._test_document = None

        return response


class DocumentTestMixin:
    auto_create_test_document_stub = False
    auto_create_test_document_type = True
    auto_upload_test_document = True
    _test_document_file_filename = TEST_FILE_SMALL_FILENAME
    _test_document_file_path = None
    _test_document_filename = TEST_FILE_SMALL_FILENAME
    _test_document_language = None
    _test_document_path = None
    auto_delete_test_document_type = True

    def setUp(self):
        super().setUp()
        Layer.invalidate_cache()

        self._test_documents = []
        self._test_document_files = []
        self._test_document_file_pages = []
        self._test_document_types = []

        if self.auto_create_test_document_type:
            self._create_test_document_type()

            if self.auto_upload_test_document:
                self._upload_test_document()
            elif self.auto_create_test_document_stub:
                self._create_test_document_stub()

    def tearDown(self):
        if self.auto_delete_test_document_type:
            for document_type in DocumentType.objects.all():
                document_type.delete()
        super().tearDown()

    def _create_test_document_stub(self, document_type=None, label=None):
        self._test_document_stub = Document.objects.create(
            document_type=document_type or self._test_document_type,
            label=label or '{}_{}'.format(
                DEFAULT_DOCUMENT_STUB_LABEL, len(self._test_documents)
            )
        )
        self._test_document = self._test_document_stub
        self._test_documents.append(self._test_document)

    def _create_test_document_type(self, label=None):
        label = label or '{}_{}'.format(
            TEST_DOCUMENT_TYPE_LABEL, len(self._test_document_types)
        )

        self._test_document_type = DocumentType.objects.create(label=label)
        self._test_document_types.append(self._test_document_type)

    def _calculate_test_document_path(self):
        if not self._test_document_path:
            self._test_document_path = os.path.join(
                settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
                'sample_documents', self._test_document_filename
            )

    def _calculate_test_document_file_path(self):
        if not self._test_document_file_path:
            self._test_document_file_path = os.path.join(
                settings.BASE_DIR, 'apps', 'documents', 'tests', 'contrib',
                'sample_documents', self._test_document_file_filename
            )

    def _upload_test_document(
        self, description=None, document_file_attributes=None,
        document_type=None, document_version_attributes=None, label=None,
        _user=None
    ):
        self._calculate_test_document_path()

        if not label:
            label = self._test_document_filename

        test_document_description = description or '{}_{}'.format(
            TEST_DOCUMENT_DESCRIPTION, len(self._test_documents)
        )

        document_type = document_type or self._test_document_type

        with open(file=self._test_document_path, mode='rb') as file_object:
            document, document_file = document_type.new_document(
                description=test_document_description,
                file_object=file_object, label=label,
                language=self._test_document_language, _user=_user
            )

        self._test_document = document
        self._test_documents.append(document)

        self._test_document_file = document_file
        self._test_document_files.append(document_file)
        self._test_document_file_pages = list(document_file.file_pages.all())
        self._test_document_file_page = document_file.file_pages.first()
        self._test_document_version = self._test_document.version_active
        self._test_document_version_page = self._test_document_version.version_pages.first()

        if document_file_attributes:
            for key, value in document_file_attributes.items():
                setattr(self._test_document_file, key, value)

            self._test_document_file.save()

        if document_version_attributes:
            for key, value in document_version_attributes.items():
                setattr(self._test_document_version, key, value)

            self._test_document_version.save()


class DocumentViewTestMixin:
    def _request_test_document_list_view(self):
        return self.get(viewname='documents:document_list')

    def _request_test_document_preview_view(self):
        return self.get(
            viewname='documents:document_preview', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_print_form_view(self):
        return self.get(
            viewname='documents:document_print_form', kwargs={
                'document_id': self._test_document.pk,
            }, data={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_print_view(self):
        return self.get(
            viewname='documents:document_print_view', kwargs={
                'document_id': self._test_document.pk,
            }, query={
                'page_group': PAGE_RANGE_ALL
            }
        )

    def _request_test_document_properties_edit_get_view(self):
        return self.get(
            viewname='documents:document_properties_edit', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_properties_view(self):
        return self.get(
            viewname='documents:document_properties', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_type_change_get_view(self):
        return self.get(
            viewname='documents:document_type_change', kwargs={
                'document_id': self._test_document.pk
            }
        )

    def _request_test_document_type_change_post_view(self):
        return self.post(
            viewname='documents:document_type_change', kwargs={
                'document_id': self._test_document.pk
            }, data={'document_type': self._test_document_types[1].pk}
        )

    def _request_test_document_multiple_type_change(self):
        return self.post(
            viewname='documents:document_multiple_type_change',
            data={
                'id_list': self._test_document.pk,
                'document_type': self._test_document_types[1].pk
            }
        )
