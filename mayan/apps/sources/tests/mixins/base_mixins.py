import json

from django.db.models import Q

from mayan.apps.documents.document_file_actions import DocumentFileActionUseNewPages
from mayan.apps.documents.tests.literals import TEST_FILE_SMALL_PATH

from ...forms import NewDocumentForm
from ...models import Source
from ...source_backends.literals import (
    DEFAULT_PERIOD_INTERVAL, SOURCE_UNCOMPRESS_CHOICE_NEVER
)

from ..literals import (
    TEST_SOURCE_BACKEND_PATH, TEST_SOURCE_BACKEND_PERIODIC_PATH,
    TEST_SOURCE_LABEL, TEST_SOURCE_LABEL_EDITED
)
from ..mocks import MockRequest


class DocumentFileUploadViewTestMixin:
    def _request_document_file_upload_get_view(self):
        return self.get(
            viewname='sources:document_file_upload', kwargs={
                'document_id': self._test_document.pk,
                'source_id': self._test_source.pk,
            }
        )

    def _request_document_file_upload_post_view(self):
        with open(file=TEST_FILE_SMALL_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_file_upload', kwargs={
                    'document_id': self._test_document.pk,
                    'source_id': self._test_source.pk,
                }, data={
                    'document-action': DocumentFileActionUseNewPages.backend_id,
                    'source-file': file_object
                }
            )

    def _request_document_file_upload_no_source_view(self):
        with open(file=TEST_FILE_SMALL_PATH, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_file_upload', kwargs={
                    'document_id': self._test_document.pk,
                }, data={
                    'document-action': DocumentFileActionUseNewPages.backend_id,
                    'source-file': file_object
                }
            )


class DocumentUploadWizardViewTestMixin:
    def _request_upload_interactive_view(self):
        return self.get(
            viewname='sources:document_upload_interactive', data={
                'document_type_id': self._test_document_type.pk,
            }
        )

    def _request_upload_wizard_view(self, document_path=TEST_FILE_SMALL_PATH):
        with open(file=document_path, mode='rb') as file_object:
            return self.post(
                viewname='sources:document_upload_interactive', kwargs={
                    'source_id': self._test_source.pk
                }, data={
                    'source-file': file_object,
                    'document_type_id': self._test_document_type.pk,
                }
            )


class InteractiveSourceBackendTestMixin:
    class MockSourceForm:
        def __init__(self, **kwargs):
            self.cleaned_data = kwargs

    def setUp(self):
        super().setUp()
        self._test_document_form = self.get_test_document_form()

    def get_test_document_form(self):
        document_form = NewDocumentForm(
            data={}, document_type=self._test_document_type
        )
        document_form.full_clean()

        return document_form

    def get_test_request(self):
        return MockRequest(user=self._test_case_user)


class SourceAPIViewTestMixin:
    def _request_test_source_create_api_view(
        self, backend_path=None, extra_data=None
    ):
        pk_list = list(Source.objects.values_list('pk', flat=True))

        data = {
            'backend_path': backend_path or TEST_SOURCE_BACKEND_PATH,
            'enabled': True,
            'label': TEST_SOURCE_LABEL
        }

        if extra_data:
            data.update(extra_data)

        response = self.post(viewname='rest_api:source-list', data=data)

        try:
            self._test_source = Source.objects.get(~Q(pk__in=pk_list))
        except Source.DoesNotExist:
            self._test_source = None

        return response

    def _request_test_source_delete_api_view(self):
        return self.delete(
            viewname='rest_api:source-detail', kwargs={
                'source_id': self._test_source.pk
            }
        )

    def _request_test_source_edit_api_view_via_patch(self):
        return self.patch(
            viewname='rest_api:source-detail', kwargs={
                'source_id': self._test_source.pk
            }, data={'label': TEST_SOURCE_LABEL_EDITED}
        )

    def _request_test_source_edit_api_view_via_put(self):
        data = {
            'backend_path': self._test_source.backend_path,
            'enabled': self._test_source.enabled,
            'label': TEST_SOURCE_LABEL_EDITED
        }

        return self.put(
            viewname='rest_api:source-detail', kwargs={
                'source_id': self._test_source.pk
            }, data=data
        )

    def _request_test_source_list_api_view(self):
        return self.get(viewname='rest_api:source-list')


class SourceTestMixin:
    _create_source_method = '_create_test_source'
    auto_create_test_source = True

    def setUp(self):
        super().setUp()
        self._test_sources = []

        if self.auto_create_test_source:
            getattr(self, self._create_source_method)()

    def _create_test_source(self, backend_path=None, backend_data=None):
        total_test_sources = len(self._test_sources)
        label = '{}_{}'.format(TEST_SOURCE_LABEL, total_test_sources)

        self._test_source = Source.objects.create(
            backend_path=backend_path or TEST_SOURCE_BACKEND_PATH,
            backend_data=json.dumps(obj=backend_data or {}),
            label=label
        )
        self._test_sources.append(self._test_source)


class SourceDocumentUploadViewTestMixin:
    def _request_source_document_upload_view_via_get(self):
        return self.get(
            viewname='sources:document_upload_interactive', kwargs={
                'source_id': self._test_source.pk
            }, data={
                'document_type_id': self._test_document_type.pk,
            }
        )


class PeriodicSourceBackendTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_periodic_source_backend'

    def _create_test_periodic_source_backend(self, extra_data=None):
        backend_data = {
            'interval': DEFAULT_PERIOD_INTERVAL
        }

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=TEST_SOURCE_BACKEND_PERIODIC_PATH,
            backend_data=backend_data
        )


class SourceViewTestMixin:
    def _request_test_source_backend_selection_view(self):
        return self.get(
            viewname='sources:source_backend_selection'
        )

    def _request_test_source_create_view(
        self, backend_path=None, extra_data=None
    ):
        pk_list = list(Source.objects.values_list('pk', flat=True))

        data = {
            'enabled': True,
            'label': TEST_SOURCE_LABEL,
            'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER
        }

        if extra_data:
            data.update(extra_data)

        response = self.post(
            kwargs={
                'backend_path': backend_path or TEST_SOURCE_BACKEND_PATH
            }, viewname='sources:source_create', data=data
        )

        try:
            self._test_source = Source.objects.get(~Q(pk__in=pk_list))
        except Source.DoesNotExist:
            self._test_source = None

        return response

    def _request_test_source_delete_view(self):
        return self.post(
            viewname='sources:source_delete', kwargs={
                'source_id': self._test_source.pk
            }
        )

    def _request_test_source_edit_view(self):
        return self.post(
            viewname='sources:source_edit', kwargs={
                'source_id': self._test_source.pk
            }, data={
                'label': TEST_SOURCE_LABEL_EDITED
            }
        )

    def _request_test_source_list_view(self):
        return self.get(viewname='sources:source_list')

    def _request_test_source_test_get_view(self):
        return self.get(
            viewname='sources:source_test', kwargs={
                'source_id': self._test_source.pk
            }
        )

    def _request_test_source_test_post_view(self):
        return self.post(
            viewname='sources:source_test', kwargs={
                'source_id': self._test_source.pk
            }
        )
