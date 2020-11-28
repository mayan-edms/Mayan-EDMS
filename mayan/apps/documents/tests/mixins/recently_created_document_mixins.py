class RecentlyCreatedDocumentAPIViewTestMixin:
    def _request_recently_created_document_list_api_view(self):
        return self.get(
            viewname='rest_api:recentlycreateddocument-list'
        )
