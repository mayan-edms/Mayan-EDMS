class DuplicatedDocumentsViewsTestMixin:
    def _request_document_duplicates_list_view(self):
        return self.get(
            viewname='documents:document_duplicates_list', kwargs={
                'document_id': self.test_documents[0].pk
            }
        )

    def _request_duplicated_document_list_view(self):
        return self.get(viewname='documents:duplicated_document_list')

    def _upload_duplicate_document(self):
        self._upload_test_document()
