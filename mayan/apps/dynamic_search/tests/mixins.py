from mayan.apps.documents.search import document_search

from ..classes import SearchBackend

from .mocks import TestSearchBackend


class SearchTestMixin:
    _test_search_index_object_name = None
    _test_search_model = None

    def _deindex_instance(self, instance):
        self.search_backend.deindex_instance(instance=instance)

    def _index_instance(self, instance):
        self.search_backend.index_instance(instance=instance)

    def setUp(self):
        super().setUp()
        # Monkeypatch the search class so that the test behavior is only
        # enabled when called from a search test.
        TestSearchBackend._test_view = self
        self.search_backend = SearchBackend.get_instance()


class SearchAPIViewTestMixin(SearchTestMixin):
    def _request_search_view(self):
        query = {'q': self.test_document.label}
        return self.get(
            viewname='rest_api:search-view', kwargs={
                'search_model_name': document_search.get_full_name()
            }, query=query
        )

    def _request_advanced_search_view(self):
        query = {'document_type__label': self.test_document.document_type.label}

        return self.get(
            viewname='rest_api:advanced-search-view', kwargs={
                'search_model_name': document_search.get_full_name()
            }, query=query
        )


class SearchToolsViewTestMixin:
    def _request_search_backend_reindex_view(self):
        return self.post(viewname='search:search_backend_reindex')


class SearchViewTestMixin(SearchTestMixin):
    def _request_search_results_view(self, data, kwargs=None, query=None):
        return self.get(
            viewname='search:results', kwargs=kwargs, data=data, query=query
        )
