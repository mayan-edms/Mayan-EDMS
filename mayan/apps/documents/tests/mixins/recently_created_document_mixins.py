class RecentlyCreatedDocumentAPIViewTestMixin:
    def _request_recently_created_document_list_api_view(self):
        return self.get(
            viewname='rest_api:recentlycreateddocument-list'
        )


class RecentlyCreatedDocumentViewTestMixin:
    def _request_test_recently_created_document_list_view(self):
        return self.get(viewname='documents:document_recently_created_list')
