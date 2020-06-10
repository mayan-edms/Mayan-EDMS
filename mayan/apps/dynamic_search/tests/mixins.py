class SearchToolsViewTestMixin:
    def _request_search_backend_reindex_view(self):
        return self.post(viewname='search:search_backend_reindex')


class SearchViewTestMixin:
    def _request_search_results_view(self, data, kwargs=None, query=None):
        return self.get(
            viewname='search:results', kwargs=kwargs, data=data, query=query
        )
