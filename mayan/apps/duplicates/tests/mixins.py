class DuplicatedDocumentAPIViewTestMixin:
    def _request_test_duplicated_document_list_api_view(self):
        return self.get(viewname='rest_api:duplicateddocument-list')

    def _request_test_document_duplicates_list_api_view(self):
        return self.get(
            viewname='rest_api:documentduplicate-list', kwargs={
                'document_id': self.test_documents[0].pk
            }
        )


class DuplicatedDocumentTestMixin:
    def _upload_duplicate_document(self):
        self._upload_test_document(label='duplicated document label')


class DuplicatedDocumentViewTestMixin:
    def _request_test_document_duplicates_list_view(self):
        return self.get(
            viewname='duplicates:document_duplicates_list', kwargs={
                'document_id': self.test_documents[0].pk
            }
        )

    def _request_test_duplicated_document_list_view(self):
        return self.get(viewname='duplicates:duplicated_document_list')
