class FileMetadataViewsTestMixin:
    def _request_document_version_driver_list_view(self):
        return self.get(
            viewname='file_metadata:document_driver_list',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_document_version_file_metadata_list_view(self):
        return self.get(
            viewname='file_metadata:document_version_driver_file_metadata_list',
            kwargs={
                'document_version_driver_id': self.test_driver.pk
            }
        )

    def _request_document_submit_view(self):
        return self.post(
            viewname='file_metadata:document_submit',
            kwargs={'document_id': self.test_document.pk}
        )

    def _request_multiple_document_submit_view(self):
        return self.post(
            viewname='file_metadata:document_multiple_submit',
            data={
                'id_list': self.test_document.pk,
            }
        )


class DocumentTypeViewsTestMixin:
    def _request_document_type_settings_view(self):
        return self.get(
            viewname='file_metadata:document_type_settings',
            kwargs={'document_type_id': self.test_document.document_type.pk}
        )

    def _request_document_type_submit_view(self):
        return self.post(
            viewname='file_metadata:document_type_submit', data={
                'document_type': self.test_document_type.pk,
            }
        )
