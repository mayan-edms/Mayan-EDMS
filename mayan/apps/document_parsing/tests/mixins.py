from mayan.apps.documents.tests.literals import TEST_FILE_HYBRID_PDF_CONTENT

from ..events import (
    event_parsing_document_file_content_deleted,
    event_parsing_document_file_finished
)
from ..models import DocumentFilePageContent


class DocumentFileContentToolsViewTestMixin:
    def _request_document_type_parsing_view(self):
        return self.post(
            viewname='document_parsing:document_type_submit', data={
                'document_type': self._test_document_type.pk
            }
        )


class DocumentFileContentTestMixin:
    auto_create_test_document_file_parsed_content = False

    def setUp(self):
        super().setUp()
        if self.auto_create_test_document_file_parsed_content:
            self._create_test_document_file_parsed_content()

    def _create_test_document_file_parsed_content(self):
        DocumentFilePageContent.objects.create(
            document_file_page=self._test_document_file_page,
            content=TEST_FILE_HYBRID_PDF_CONTENT
        )
        event_parsing_document_file_finished.commit(
            action_object=self._test_document_file_page.document_file.document,
            target=self._test_document_file_page.document_file
        )

    def _do_test_document_file_parsed_content_delete(self):
        DocumentFilePageContent.objects.delete_content_for(
            document_file=self._test_document_file
        )
        event_parsing_document_file_content_deleted.commit(
            action_object=self._test_document_file.document,
            target=self._test_document_file
        )


class DocumentFileContentViewTestMixin:
    def _request_test_document_file_content_single_delete_view(self):
        return self.post(
            viewname='document_parsing:document_file_content_single_delete',
            kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )

    def _request_test_document_file_content_multiple_delete_view(self):
        return self.post(
            viewname='document_parsing:document_file_content_multiple_delete',
            data={
                'id_list': self._test_document_file.pk
            }
        )

    def _request_test_document_file_content_download_view(self):
        return self.get(
            viewname='document_parsing:document_file_content_download',
            kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )

    def _request_test_document_file_content_view(self):
        return self.get(
            'document_parsing:document_file_content_view', kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )

    def _request_test_document_file_page_content_view(self):
        return self.get(
            viewname='document_parsing:document_file_page_content_view',
            kwargs={
                'document_file_page_id': self._test_document_file.pages.first().pk,
            }
        )

    def _request_test_document_file_parsing_submit_view(self):
        return self.post(
            viewname='document_parsing:document_file_parsing_single_submit', kwargs={
                'document_file_id': self._test_document_file.pk
            }
        )

    def _request_test_document_parsing_submit_view(self):
        return self.post(
            viewname='document_parsing:document_parsing_single_submit', kwargs={
                'document_id': self._test_document.pk
            }
        )


class DocumentFilePageContentAPITestMixin:
    def _request_document_file_page_content_api_view(self):
        return self.get(
            viewname='rest_api:document-file-page-content-view', kwargs={
                'document_id': self._test_document.pk,
                'document_file_id': self._test_document_file.pk,
                'document_file_page_id': self._test_document_file.pages.first().pk
            }
        )


class DocumentTypeContentViewTestMixin:
    def _request_test_document_type_parsing_settings_view(self):
        return self.get(
            viewname='document_parsing:document_type_parsing_settings',
            kwargs={'document_type_id': self._test_document_type.pk}
        )


class DocumentTypeParsingSettingsAPIViewTestMixin():
    def _request_document_type_parsing_settings_details_api_view(self):
        return self.get(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'document_type_id': self._test_document_type.pk}
        )

    def _request_document_type_parsing_settings_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'document_type_id': self._test_document_type.pk},
            data={'auto_parsing': True}
        )

    def _request_document_type_parsing_settings_put_api_view(self):
        return self.put(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'document_type_id': self._test_document_type.pk},
            data={'auto_parsing': True}
        )
