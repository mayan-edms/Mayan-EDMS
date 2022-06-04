class DocumentTypeViewTestMixin:
    def _request_document_type_file_metadata_settings_view(self):
        return self.get(
            viewname='file_metadata:document_type_file_metadata_settings',
            kwargs={'document_type_id': self._test_document.document_type.pk}
        )

    def _request_document_type_file_metadata_submit_view(self):
        return self.post(
            viewname='file_metadata:document_type_file_metadata_submit', data={
                'document_type': self._test_document_type.pk,
            }
        )


class FileMetadataViewTestMixin:
    def _request_document_file_metadata_driver_list_view(self):
        return self.get(
            viewname='file_metadata:document_file_metadata_driver_list',
            kwargs={'document_file_id': self._test_document_file.pk}
        )

    def _request_document_file_metadata_list_view(self):
        return self.get(
            viewname='file_metadata:document_file_metadata_driver_attribute_list',
            kwargs={
                'document_file_driver_id': self.test_driver.pk
            }
        )

    def _request_document_file_metadata_single_submit_view(self):
        return self.post(
            viewname='file_metadata:document_file_metadata_single_submit',
            kwargs={'document_file_id': self._test_document_file.pk}
        )

    def _request_document_file_multiple_submit_view(self):
        return self.post(
            viewname='file_metadata:document_file_metadata_multiple_submit',
            data={
                'id_list': self._test_document_file.pk,
            }
        )
