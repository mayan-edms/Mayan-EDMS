class TrashedDocumentAPIViewTestMixin:
    def _request_test_document_trash_api_view(self):
        return self.delete(
            viewname='rest_api:document-detail', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_delete_api_view(self):
        return self.delete(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_detail_api_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-detail', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_image_api_view(self):
        return self.get(
            viewname='rest_api:documentversionpage-image', kwargs={
                'document_id': self.test_document.pk,
                'document_version_id': self.test_document_version.pk,
                'document_version_page_id': self.test_document_version_page.pk
            }
        )

    def _request_test_trashed_document_list_api_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-list'
        )

    def _request_test_trashed_document_restore_via_get_api_view(self):
        return self.get(
            viewname='rest_api:trasheddocument-restore', kwargs={
                'document_id': self.test_document.pk
            }, query={'format': 'api'}
        )

    def _request_test_trashed_document_restore_via_post_api_view(self):
        return self.post(
            viewname='rest_api:trasheddocument-restore', kwargs={
                'document_id': self.test_document.pk
            }
        )


class TrashedDocumentViewTestMixin:
    def _request_test_document_trash_get_view(self):
        return self.get(
            viewname='documents:document_trash', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_trash_post_view(self):
        return self.post(
            viewname='documents:document_trash', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_empty_trash_view(self):
        return self.post(viewname='documents:trash_can_empty')

    def _request_test_trashed_document_restore_get_view(self):
        return self.get(
            viewname='documents:document_restore', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_restore_post_view(self):
        return self.post(
            viewname='documents:document_restore', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_delete_get_view(self):
        return self.get(
            viewname='documents:document_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_delete_post_view(self):
        return self.post(
            viewname='documents:document_delete', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_trashed_document_list_view(self):
        return self.get(viewname='documents:document_list_deleted')
