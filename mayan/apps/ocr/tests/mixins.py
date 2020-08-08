class DocumentOCRViewTestMixin(object):
    def _request_document_content_view(self):
        return self.get(
            viewname='ocr:document_ocr_content', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_document_content_delete_view(self):
        return self.post(
            viewname='ocr:document_ocr_content_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_document_page_content_view(self):
        return self.get(
            viewname='ocr:document_page_ocr_content', kwargs={
                'document_page_id': self.test_document.pages.first().pk
            }
        )

    def _request_document_submit_view(self):
        return self.post(
            viewname='ocr:document_submit', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_multiple_document_submit_view(self):
        return self.post(
            viewname='ocr:document_submit_multiple', data={
                'id_list': self.test_document.pk,
            }
        )

    def _request_document_ocr_download_view(self):
        return self.get(
            viewname='ocr:document_ocr_download', kwargs={
                'document_id': self.test_document.pk
            }
        )


class DocumentTypeOCRSettingsAPIViewTestMixin():
    def _request_document_type_ocr_settings_details_api_view(self):
        return self.get(
            viewname='rest_api:document-type-ocr-settings-view',
            kwargs={'pk': self.test_document_type.pk}
        )

    def _request_document_type_ocr_settings_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-type-ocr-settings-view',
            kwargs={'pk': self.test_document_type.pk},
            data={'auto_ocr': True}
        )

    def _request_document_type_ocr_settings_put_api_view(self):
        return self.put(
            viewname='rest_api:document-type-ocr-settings-view',
            kwargs={'pk': self.test_document_type.pk},
            data={'auto_ocr': True}
        )


class DocumentTypeOCRViewTestMixin(object):
    def _request_document_type_ocr_settings_view(self):
        return self.get(
            viewname='ocr:document_type_ocr_settings', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )
