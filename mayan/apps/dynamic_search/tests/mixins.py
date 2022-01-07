from mayan.apps.documents.search import document_search

from ..classes import SearchBackend, SearchModel

from .backends import TestSearchBackend


class SearchTestMixin:
    def _deindex_instance(self, instance):
        self.search_backend.deindex_instance(instance=instance)

    def _index_instance(self, instance):
        self.search_backend.index_instance(instance=instance)

    def _setup_test_model_search(self):
        """
        This method allows tests to add model search configurations and
        not have to import and initialize the SearchBackend.
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        TestSearchBackend._test_class = cls
        cls.search_backend = SearchBackend.get_instance()

    @classmethod
    def tearDownClass(cls):
        cls.search_backend.tear_down()
        cls.search_backend.close()
        super().tearDownClass()

    def setUp(self):
        self._existing_search_models = SearchModel._registry.copy()
        super().setUp()
        # Monkeypatch the search class so that the test behavior is only
        # enabled when called from a search test.
        self._setup_test_model_search()
        SearchBackend._enable()

    def tearDown(self):
        SearchBackend._disable()
        super().tearDown()
        SearchModel._registry = self._existing_search_models


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


class SearchToolsViewTestMixin(SearchTestMixin):
    def _request_search_backend_reindex_view(self):
        return self.post(viewname='search:search_backend_reindex')


class SearchViewTestMixin(SearchTestMixin):
    def _request_search_results_view(self, data, kwargs=None, query=None):
        return self.get(
            viewname='search:results', kwargs=kwargs, data=data, query=query
        )
