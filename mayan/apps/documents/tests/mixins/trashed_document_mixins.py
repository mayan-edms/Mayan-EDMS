class TrashedDocumentAPIViewTestMixin:
    def _request_test_document_api_trash_view(self):
        return self.delete(
            viewname='rest_api:document-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_delete_view(self):
        return self.delete(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_detail_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_trashed_document_api_image_view(self):
        latest_file = self.test_document.latest_file

        return self.get(
            viewname='rest_api:documentpage-image', kwargs={
                'pk': latest_file.document_id,
                'file_pk': latest_file.pk,
                'page_pk': latest_file.pages.first().pk
            }
        )

    def _request_test_trashed_document_api_list_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-list'
        )

    def _request_test_trashed_document_api_restore_view(self):
        return self.post(
            viewname='rest_api:trasheddocument-restore', kwargs={
                'pk': self.test_document.pk
            }
        )


class TrashedDocumentViewTestMixin:
    def _request_document_trash_get_view(self):
        return self.get(
            viewname='documents:document_trash', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_document_trash_post_view(self):
        return self.post(
            viewname='documents:document_trash', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_empty_trash_view(self):
        return self.post(viewname='documents:trash_can_empty')

    def _request_trashed_document_restore_get_view(self):
        return self.get(
            viewname='documents:document_restore', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_restore_post_view(self):
        return self.post(
            viewname='documents:document_restore', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_delete_get_view(self):
        return self.get(
            viewname='documents:document_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_delete_post_view(self):
        return self.post(
            viewname='documents:document_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_trashed_document_list_view(self):
        return self.get(viewname='documents:document_list_deleted')
