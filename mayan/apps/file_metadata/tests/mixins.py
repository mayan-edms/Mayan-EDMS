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


class FileMetadataViewsTestMixin:
    def _request_document_file_driver_list_view(self):
        return self.get(
            viewname='file_metadata:document_file_driver_list',
            kwargs={'document_file_id': self.test_document_file.pk}
        )

    def _request_document_file_metadata_list_view(self):
        return self.get(
            viewname='file_metadata:document_file_driver_file_metadata_list',
            kwargs={
                'document_file_driver_id': self.test_driver.pk
            }
        )

    def _request_document_file_submit_single_view(self):
        return self.post(
            viewname='file_metadata:document_file_submit_single',
            kwargs={'document_file_id': self.test_document_file.pk}
        )

    def _request_document_file_submit_multiple_view(self):
        return self.post(
            viewname='file_metadata:document_file_submit_multiple',
            data={
                'id_list': self.test_document_file.pk,
            }
        )
