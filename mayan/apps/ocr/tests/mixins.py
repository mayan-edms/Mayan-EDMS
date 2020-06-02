
class DocumentOCRViewTestMixin:
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


class DocumentTypeOCRViewTestMixin:
    def _request_document_type_ocr_settings_view(self):
        return self.get(
            viewname='ocr:document_type_ocr_settings', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )
