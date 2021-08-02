from ..models import DocumentVersionPageOCRContent

from .literals import TEST_DOCUMENT_VERSION_OCR_CONTENT


class DocumentTypeOCRSettingsAPIViewTestMixin:
    def _request_test_document_type_ocr_settings_details_api_view(self):
        return self.get(
            viewname='rest_api:document-type-ocr-settings-view',
            kwargs={'document_type_id': self.test_document_type.pk}
        )

    def _request_test_document_type_ocr_settings_patch_api_view(self):
        return self.patch(
            viewname='rest_api:document-type-ocr-settings-view',
            kwargs={'document_type_id': self.test_document_type.pk},
            data={'auto_ocr': True}
        )

    def _request_test_document_type_ocr_settings_put_api_view(self):
        return self.put(
            viewname='rest_api:document-type-ocr-settings-view',
            kwargs={'document_type_id': self.test_document_type.pk},
            data={'auto_ocr': True}
        )


class DocumentTypeOCRViewTestMixin:
    def _request_test_document_type_ocr_settings_view(self):
        return self.get(
            viewname='ocr:document_type_ocr_settings', kwargs={
                'document_type_id': self.test_document_type.pk
            }
        )

    def _request_document_type_ocr_submit_view(self):
        return self.post(
            viewname='ocr:document_type_submit', data={
                'document_type': [self.test_document_type.pk]
            }
        )


class DocumentVersionOCRAPIViewTestMixin:
    def _request_test_document_ocr_submit_api_view(self):
        return self.post(
            viewname='rest_api:document-ocr-submit-view',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_test_document_version_ocr_submit_api_view(self):
        return self.post(
            viewname='rest_api:document-version-ocr-submit-view', kwargs={
                'document_id': self.test_document.pk,
                'document_version_id': self.test_document.version_active.pk
            }
        )


class DocumentVersionPageOCRAPIViewTestMixin:
    def _request_test_document_version_page_ocr_content_detail_api_view(self):
        return self.get(
            viewname='rest_api:document-version-page-ocr-content-detail-view', kwargs={
                'document_id': self.test_document.pk,
                'document_version_id': self.test_document.version_active.pk,
                'document_version_page_id': self.test_document.version_active.pages.first().pk,
            }
        )


class DocumentVersionOCRTestMixin:
    def _create_test_document_version_ocr_content(self):
        DocumentVersionPageOCRContent.objects.create(
            document_version_page=self.test_document_version.pages.first(),
            content=TEST_DOCUMENT_VERSION_OCR_CONTENT
        )


class DocumentVersionOCRViewTestMixin:
    def _request_test_document_version_ocr_content_view(self):
        return self.get(
            viewname='ocr:document_version_ocr_content_view', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )

    def _request_test_document_version_ocr_content_delete_view(self):
        return self.post(
            viewname='ocr:document_version_ocr_content_delete', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )

    def _request_test_document_version_ocr_error_list_view(self):
        return self.get(
            viewname='ocr:document_version_ocr_error_list', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )

    def _request_test_document_version_ocr_submit_view(self):
        return self.post(
            viewname='ocr:document_version_ocr_submit', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )

    def _request_test_document_version_multiple_ocr_submit_view(self):
        return self.post(
            viewname='ocr:document_version_multiple_ocr_submit', data={
                'id_list': self.test_document_version.pk,
            }
        )

    def _request_test_document_version_ocr_download_view(self):
        return self.get(
            viewname='ocr:document_version_ocr_download', kwargs={
                'document_version_id': self.test_document_version.pk
            }
        )


class DocumentVersionPageOCRViewTestMixin:
    def _request_test_document_version_page_ocr_content_detail_view(self):
        return self.get(
            viewname='ocr:document_version_page_ocr_content_detail_view', kwargs={
                'document_version_page_id': self.test_document_version.pages.first().pk
            }
        )
