class RecentlyAccessedDocumentAPIViewTestMixin:
    def _request_recently_accessed_document_list_api_view(self):
        return self.get(
            viewname='rest_api:recentlyaccesseddocument-list'
        )
