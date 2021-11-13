from mayan.apps.documents.search import document_search

from ..classes import SearchBackend


class SearchAPIViewTestMixin:
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


class SearchTestMixin:
    _test_search_index_object_name = None
    _test_search_model = None

    def _deindex_instance(self, instance):
        self.search_backend.deindex_instance(instance=instance)

    def _index_instance(self, instance):
        self.search_backend.index_instance(instance=instance)

    def do_test_search(self, terms=None, query=None):
        if self._test_search_index_object_name:
            self.search_backend.index_instance(
                instance=getattr(self, self._test_search_index_object_name)
            )

        query = query or {'q': terms}

        return self.search_backend.search(
            search_model=self._test_search_model, query=query,
            user=self._test_case_user
        )

    def setUp(self):
        super().setUp()

        self.search_backend = SearchBackend.get_instance(
            extra_kwargs={'_search_test': True}
        )

    def tearDown(self):
        if hasattr(self.search_backend, '_cleanup'):
            self.search_backend._cleanup()

        super().tearDown()


class SearchToolsViewTestMixin:
    def _request_search_backend_reindex_view(self):
        return self.post(viewname='search:search_backend_reindex')


class SearchViewTestMixin:
    def _request_search_results_view(self, data, kwargs=None, query=None):
        return self.get(
            viewname='search:results', kwargs=kwargs, data=data, query=query
        )
