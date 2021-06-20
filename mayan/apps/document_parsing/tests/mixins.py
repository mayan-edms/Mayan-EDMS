from ..models import DocumentFilePageContent

from .literals import TEST_DOCUMENT_CONTENT


class DocumentFileContentToolsViewsTestMixin:
    def _request_document_parsing_error_list_view(self):
        return self.get(viewname='document_parsing:error_list')

    def _request_document_type_parsing_view(self):
        return self.post(
            viewname='document_parsing:document_type_submit', data={
                'document_type': self.test_document_type.pk
            }
        )


class DocumentFileContentTestMixin:
    def setUp(self):
        super().setUp()
        self._create_test_document_file_parsed_content()

    def _create_test_document_file_parsed_content(self):
        DocumentFilePageContent.objects.create(
            document_file_page=self.test_document_file_page,
            content=TEST_DOCUMENT_CONTENT
        )


class DocumentFileContentViewTestMixin:
    def _request_test_document_file_content_delete_view(self):
        return self.post(
            viewname='document_parsing:document_file_content_delete',
            kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_file_content_download_view(self):
        return self.get(
            viewname='document_parsing:document_file_content_download',
            kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_file_content_view(self):
        return self.get(
            'document_parsing:document_file_content_view', kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_file_page_content_view(self):
        return self.get(
            viewname='document_parsing:document_file_page_content_view',
            kwargs={
                'document_file_page_id': self.test_document_file.pages.first().pk,
            }
        )

    def _request_test_document_file_parsing_error_list_view(self):
        return self.get(
            viewname='document_parsing:document_file_parsing_error_list',
            kwargs={
                'document_file_id': self.test_document_file.pk,
            }
        )

    def _request_test_document_file_parsing_submit_view(self):
        return self.post(
            viewname='document_parsing:document_file_submit', kwargs={
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_parsing_submit_view(self):
        return self.post(
            viewname='document_parsing:document_submit', kwargs={
                'document_id': self.test_document.pk
            }
        )


class DocumentParsingAPITestMixin:
    def _request_document_file_page_content_api_view(self):
        return self.get(

            viewname='rest_api:document-file-page-content-view', kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'document_file_page_id': self.test_document_file.pages.first().pk
            }
        )


class DocumentTypeContentViewsTestMixin:
    def _request_test_document_type_parsing_settings_view(self):
        return self.get(
            viewname='document_parsing:document_type_parsing_settings',
            kwargs={'document_type_id': self.test_document_type.pk}
        )


class DocumentTypeParsingSettingsAPIViewTestMixin():
    def _request_document_type_parsing_settings_details_api_view(self):
        return self.get(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'document_type_id': self.test_document_type.pk}
        )

    def _request_document_type_parsing_settings_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'document_type_id': self.test_document_type.pk},
            data={'auto_parsing': True}
        )

    def _request_document_type_parsing_settings_put_api_view(self):
        return self.put(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'document_type_id': self.test_document_type.pk},
            data={'auto_parsing': True}
        )
