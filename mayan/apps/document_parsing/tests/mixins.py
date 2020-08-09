class DocumentContentToolsViewsTestMixin:
    def _request_document_parsing_error_list_view(self):
        return self.get(viewname='document_parsing:error_list')

    def _request_document_parsing_tool_view(self):
        return self.post(
            viewname='document_parsing:document_type_submit', data={
                'document_type': self.test_document_type.pk
            }
        )


class DocumentContentViewTestMixin:
    def _request_test_document_content_delete_view(self):
        return self.post(
            viewname='document_parsing:document_content_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_content_download_view(self):
        return self.get(
            viewname='document_parsing:document_content_download', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_content_view(self):
        return self.get(
            'document_parsing:document_content', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_page_content_view(self):
        return self.get(
            viewname='document_parsing:document_page_content', kwargs={
                'document_page_id': self.test_document.pages.first().pk,
            }
        )

    def _request_test_document_parsing_error_list_view(self):
        return self.get(
            viewname='document_parsing:document_parsing_error_list', kwargs={
                'document_id': self.test_document.pk,
            }
        )


class DocumentTypeContentViewsTestMixin:
    def _request_test_document_type_parsing_settings(self):
        return self.get(
            viewname='document_parsing:document_type_parsing_settings',
            kwargs={'document_type_id': self.test_document_type.pk}
        )


class DocumentTypeParsingSettingsAPIViewTestMixin():
    def _request_document_type_parsing_settings_details_api_view(self):
        return self.get(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'pk': self.test_document_type.pk}
        )

    def _request_document_type_parsing_settings_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'pk': self.test_document_type.pk},
            data={'auto_parsing': True}
        )

    def _request_document_type_parsing_settings_put_api_view(self):
        return self.put(
            viewname='rest_api:document-type-parsing-settings-view',
            kwargs={'pk': self.test_document_type.pk},
            data={'auto_parsing': True}
        )
