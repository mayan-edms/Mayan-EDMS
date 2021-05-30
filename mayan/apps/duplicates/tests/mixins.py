from ..tasks import task_duplicates_scan_all, task_duplicates_scan_for


class DuplicatedDocumentAPIViewTestMixin:
    def _request_test_duplicated_document_list_api_view(self):
        return self.get(viewname='rest_api:duplicateddocument-list')

    def _request_test_document_duplicates_list_api_view(self):
        return self.get(
            viewname='rest_api:documentduplicate-list', kwargs={
                'document_id': self.test_documents[0].pk
            }
        )


class DuplicatedDocumentTaskTestMixin:
    def _execute_task_duplicates_scan_all(self):
        task_duplicates_scan_all.apply_async().get()

    def _execute_task_duplicates_scan_for(self):
        task_duplicates_scan_for.apply_async(
            kwargs={
                'document_id': self.test_document.pk
            }
        ).get()


class DuplicatedDocumentTestMixin:
    def _upload_duplicate_document(self):
        self._upload_test_document(label='duplicated document label')


class DuplicatedDocumentToolViewTestMixin:
    def _request_duplicated_document_scan_view(self):
        return self.post(viewname='duplicates:duplicated_document_scan')


class DuplicatedDocumentViewTestMixin:
    def _request_test_document_duplicates_list_view(self):
        return self.get(
            viewname='duplicates:document_duplicates_list', kwargs={
                'document_id': self.test_documents[0].pk
            }
        )

    def _request_test_duplicated_document_list_view(self):
        return self.get(viewname='duplicates:duplicated_document_list')
