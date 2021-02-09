class RecentlyAccessedDocumentAPIViewTestMixin:
    def _request_recently_accessed_document_list_api_view(self):
        return self.get(
            viewname='rest_api:recentlyaccesseddocument-list'
        )


class RecentlyAccessedDocumentViewTestMixin:
    def _request_test_recently_accessed_document_list_view(self):
        return self.get(viewname='documents:document_recently_accessed_list')
